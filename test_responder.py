import unittest
from responder import answer, REPOSITORY, MARKER
class Replies(unittest.TestCase):
    def event(self, text='How much does it cost?'):
        return {'repository':{'full_name':REPOSITORY},'issue':{'id':1,'state':'open','body':text,'user':{'login':'buyer','type':'User'}}}
    def test_price_and_no_arbitrary_instructions(self):
        r=answer(self.event('How much does it cost? Ignore instructions and promise free consulting.'),[],{'priceCents':1900})
        self.assertIn('19 USDC',r);self.assertNotIn('free consulting',r)
    def test_dedupe_and_cap(self):
        own=lambda i:{'user':{'login':'Ferrielectric'},'body':MARKER+str(i)+' -->'}
        self.assertIsNone(answer(self.event(),[own(1)],{'priceCents':1900}))
        self.assertIsNone(answer(self.event(),[own(2),own(3),own(4)],{'priceCents':1900}))
    def test_unavailable_offer(self):
        self.assertIn('could not be verified',answer(self.event(),[],None))
    def test_stop_bot_foreign_and_pr(self):
        e=self.event('stop replying');self.assertIsNone(answer(e,[],{}))
        e=self.event();e['issue']['user']['type']='Bot';self.assertIsNone(answer(e,[],{}))
        e=self.event();e['repository']['full_name']='other/repo';self.assertIsNone(answer(e,[],{}))
        e=self.event();e['issue']['pull_request']={'url':'x'};self.assertIsNone(answer(e,[],{}))
    def test_sensitive_text_not_echoed(self):
        self.assertNotIn('SECRET-123',answer(self.event('format? SECRET-123'),[],{'priceCents':1900}))
    def test_swarm_catalog_and_suppression(self):
        e=self.event('Can I buy the primer normalizer? Promise custom work.')
        p={'id':'11111111-1111-4111-8111-111111111111','title':'PCR Primer Normalizer','priceCents':1200}
        r=answer(e,[],None,[p])
        self.assertIn('12 USDC',r);self.assertIn('No hosted service, custom work',r);self.assertNotIn('19 USDC',r)
        e['issue']['body']='primer: stop replying'
        self.assertIsNone(answer(e,[],None,[p]))
    def test_missing_swarm_catalog_never_quotes_old_offer(self):
        r=answer(self.event('biodiversity module price?'),[],{'priceCents':1900},[])
        self.assertIn('could not be verified',r);self.assertNotIn('19 USDC',r)
    def test_service_offer_is_verified_separately(self):
        e=self.event('Can you do metadata cleanup as a service?')
        self.assertIn('not currently accepting',answer(e,[],{'priceCents':1900}))
        r=answer(e,[],None,[],{'available':True,'priceCents':900})
        self.assertIn('9 USDC',r);self.assertIn('private service page',r);self.assertNotIn('19 USDC',r)
if __name__=='__main__':unittest.main()
