# Guilded metadata service and tools

## Let us process the file for you

[Metadata cleanup and exception report](https://guilded.dev/services/metadata-cleanup/?source=github) costs 9 USDC for one JSON file of 1 to 25 records, at most 10 KB. We prepare the result before requesting payment. Receive normalized records, a change log and an exception report without installing software. Only surrounding whitespace in documented text fields is changed; uncertain values are preserved. No scientific certification, biological interpretation, custom work or ongoing support. Check live availability and exact limits on the service page. Never upload private datasets in GitHub issues. Ask a question here using “cleanup service.”

## Earlier software experiment

The packages below remain available under their original terms. The current pilot focuses on delivering the cleanup outcome.

### Environmental DNA Metadata Validator

A small local tool for checking environmental DNA sample metadata before analysis. It flags missing fields, duplicate sample IDs, invalid coordinates, inconsistent counts and control failures in JSON records.

**[See the example and get the package for 19 USDC](https://guilded.dev/products/edna-metadata-validator/?source=github)** · **[Ask a product question](https://github.com/Ferrielectric/edna-metadata-validator/issues/new/choose)**

This repository contains public examples, documentation and an automated product question responder. The validator source and its acceptance tests are delivered with the paid package. These examples are synthetic, not customer data or scientific findings.

## More local data tools

[Browse the live swarm product catalog](PRODUCTS.md), including the PCR Primer Normalizer and eDNA Biodiversity Integration Module. Each has its own examples, limitations and purchase terms. Ask a question here using the product name; the automated responder checks current catalog availability.

## See an actual result

[Example input](examples/input.json) includes three records: one passes the documented rules, one needs a confirmation method, and one has an invalid coordinate and count. [Expected output](examples/output.json) was produced by version 1 of the validator.

```json
{ "total": 3, "ready": 1, "review": 1, "invalid": 1 }
```

`ready` means the record passed these rules. It does not mean a species was detected reliably or that a dataset has scientific approval.

## What is included

The package includes JavaScript source, nine acceptance tests, an example dataset, usage instructions and a perpetual license to use and modify this version for your own work. Run it locally with Node.js 20 or later. It has no dependencies or subscription. Your sample data stays on your machine.

```sh
node index.mjs input.json results.json
node --test acceptance.test.mjs
```

The command refuses to overwrite an existing output file. Your JSON records must use the documented field names; this is not an automatic importer for arbitrary spreadsheets.

## Checks and limits

Required fields: `sampleId`, `siteId`, `collectedAt`, `latitude`, `longitude`, `targetTaxon`, `assay`, `replicateCount`, `detectionCount`, `positiveControl`, `negativeControl`.

Positive detections also need `confirmationMethod` to avoid a review warning. Dates must be JavaScript parseable; this is not a strict date standard. Replicate counts must be integers from 1 to 100, detection counts cannot exceed replicates, coordinates must be in range, and both control flags must be boolean true. Sample IDs are compared exactly.

Built with AI assistance and developer review. The tool does not analyze DNA, validate taxonomy, certify scientific results or integrate with ecocomDP. Custom work, future features and ongoing support are not included. Tests cover documented examples rather than every possible dataset.

## Price and delivery

The current offer is **19 USDC on Base**. Review the exact terms at checkout. Payment requires a compatible wallet; network fees are separate. After the matching payment is finalized, your private order page releases the package. Keep that private link. Do not post it in an issue.

The current offer expires on November 12, 2026. Checkout determines current availability. Refund requests for failures of documented checks can be submitted through the private order page within 14 days of payment and are reviewed individually. No automatic refund transfer is promised.

## Questions before buying

Open a product question using the issue form. Guilded's automated responder can explain scope, input format, price, licensing and delivery using the published terms. It cannot negotiate, promise custom work, take payment in a comment or confirm a payment from a screenshot. Do not post private datasets, access tokens, order links or personal information.

These public examples and documentation may be copied for evaluation. This permission does not grant rights to the separate paid validator package.
