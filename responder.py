"""Bounded public product Q&A. No model, arbitrary commands, payment or private data."""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone

REPOSITORY = 'Ferrielectric/edna-metadata-validator'
PRODUCT = 'b492b389-528e-4de9-8852-d894929e6273'
OFFER = 'https://guilded.dev/products/edna-metadata-validator/?source=github-qa'
MARKER = '<!-- guilded-validator-answer:'

def answer(event, comments, offer, catalog=None):
    if event.get('repository', {}).get('full_name') != REPOSITORY:
        return None
    issue = event.get('issue', {})
    incoming = event.get('comment') or issue
    if issue.get('pull_request') or issue.get('state') != 'open':
        return None
    if incoming.get('user', {}).get('type') == 'Bot':
        return None
    if event.get('comment') and incoming.get('user', {}).get('login') != issue.get('user', {}).get('login'):
        return None
    text = str(incoming.get('body') or '')[:12000]
    if MARKER in text:
        return None
    if re.search(r'\b(unsubscribe|stop replying|do not reply|stop contacting)\b', text, re.I):
        return None
    marker = MARKER + str(incoming.get('id')) + ' -->'
    own = [c for c in comments if c.get('user', {}).get('login') == 'Ferrielectric' and MARKER in str(c.get('body'))]
    if any(marker in str(c.get('body')) for c in own) or len(own) >= 3:
        return None
    if any(re.search(r'\b(unsubscribe|stop replying|do not reply|stop contacting)\b', str(c.get('body') or ''), re.I) for c in comments if c.get('user', {}).get('login') == issue.get('user', {}).get('login')):
        return None
    full_text = str(issue.get('title') or '') + ' ' + text
    if re.search(r'primer|biodiversity|integration module|swarm|catalog', full_text, re.I):
        products = catalog or []
        lines = []
        for p in products[:3]:
            if not re.fullmatch(r'[a-f0-9-]{36}', str(p.get('id',''))) or not isinstance(p.get('priceCents'), int) or not 100 <= p['priceCents'] <= 1900:
                continue
            title = re.sub(r'[^a-zA-Z0-9 ,().]', '', str(p.get('title','')))[:100]
            lines.append(f"[{title}](https://guilded.dev/products/?product={p['id']}&source=github-qa): {p['priceCents']/100:g} USDC.")
        return 'Guilded automated product response\n\n' + ('\n\n'.join(lines) if lines else 'The current swarm catalog could not be verified. Check https://guilded.dev/products/ for availability.') + '\n\nThese are downloadable local source packages created by the swarm. Review each offer’s illustrated input and output before buying. Automated VM tests are not scientific certification. No hosted service, custom work or ongoing support is included. Payment uses USDC on Base, with separate network fees. Delivery follows verified payment on your private order page. Do not post private data or order links here.\n\n' + marker
    if not offer or offer.get('priceCents') != 1900:
        return 'Guilded automated response: the current offer could not be verified, so I cannot quote an active sale. Please check [offer availability](' + OFFER + ').\n\n' + marker
    sections = []
    if re.search(r'price|cost|buy|purchase|pay|wallet|usdc|card', text, re.I):
        sections.append('The current package is 19 USDC on Base, paid from a compatible wallet. Network fees are separate. Card checkout is not currently available. Review and sign the exact order terms on the checkout page before paying.')
    if re.search(r'format|csv|json|field|spreadsheet|input|schema|example', text, re.I):
        sections.append('Input is a JSON array using the documented field names. There is no CSV or spreadsheet importer. See [synthetic input and actual output](https://github.com/' + REPOSITORY + '/tree/main/examples). Sample IDs must be unique; coordinates, counts and control flags are checked. Positive detections without a confirmation method receive a review warning.')
    if re.search(r'license|licence|source|commercial|redistribut|resell', text, re.I):
        sections.append('The paid package includes JavaScript source and tests, with a perpetual license to use and modify this version for your own work. Resale and redistribution of the package are not included. The public examples are separate from the paid source.')
    if re.search(r'install|node|run|offline|upload|privacy|data', text, re.I):
        sections.append('It runs locally with Node.js 20 or later and no dependencies. Your dataset does not need to be uploaded. Run `node index.mjs input.json results.json`; the command refuses to overwrite an existing output file.')
    if re.search(r'refund|delivery|download|support|paid|receipt', text, re.I):
        sections.append('Delivery appears on your private order page after the matching Base USDC payment is finalized. Retain that link and keep it private. Refund requests for failures of documented checks are reviewed through that page within 14 days of payment. I cannot verify payments or issue refunds from a public comment.')
    if re.search(r'scientific|certif|ecocom|taxonomy|dna|integrat|custom|reliab', text, re.I) or not sections:
        sections.append('This is a small metadata checker, built with AI assistance and developer review. It does not analyze DNA, establish detection reliability, validate taxonomy or certify scientific results. ecocomDP integration, custom work, future features and ongoing support are not included.')
    return 'Guilded automated product response\n\n' + '\n\n'.join(sections[:4]) + '\n\n[Read the full offer and purchase terms](' + OFFER + '). No purchase is made by opening that page.\n\n' + marker

def main():
    if os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        raise RuntimeError('Unexpected repository')
    event = json.load(open(os.environ['GITHUB_EVENT_PATH']))
    number = event.get('issue', {}).get('number')
    if not isinstance(number, int) or number < 1:
        return
    token = os.environ['GH_TOKEN']
    def api(path, body=None):
        req = urllib.request.Request('https://api.github.com/repos/' + REPOSITORY + path, data=None if body is None else json.dumps(body).encode(), headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'Guilded-validator-support'})
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.load(response)
    identity_request = urllib.request.Request('https://api.github.com/user', headers={'Authorization':'Bearer '+token,'User-Agent':'Guilded-validator-support'})
    with urllib.request.urlopen(identity_request, timeout=20) as response:
        if json.load(response).get('login') != 'Ferrielectric':
            raise RuntimeError('Ferrielectric authentication required')
    if api('').get('owner', {}).get('login') != 'Ferrielectric':
        raise RuntimeError('Ferrielectric repository required')
    comments = api(f'/issues/{number}/comments?per_page=100')
    if len(comments) >= 100:
        return
    offer = None
    try:
        req = urllib.request.Request('https://guilded.dev/api/workspace?route=sales-product',data=json.dumps({'productId':PRODUCT}).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=20) as response:
            offer = json.load(response)
        expiry = datetime.fromisoformat(offer['expiresAt'].replace('Z','+00:00'))
        if expiry <= datetime.now(timezone.utc):
            offer = None
    except Exception:
        offer = None
    catalog = []
    try:
        with urllib.request.urlopen('https://guilded.dev/api/workspace?route=sales-catalog', timeout=20) as response:
            catalog = [p for p in json.load(response).get('products', []) if datetime.fromisoformat(p['expiresAt'].replace('Z','+00:00')) > datetime.now(timezone.utc)]
    except Exception:
        pass
    body = answer(event,comments,offer,catalog)
    if body:
        result = api(f'/issues/{number}/comments',{'body':body})
        print(json.dumps({'commentUrl':result['html_url'],'issue':number,'automated':True}))
    else:
        print('No response required')

if __name__ == '__main__':
    main()
