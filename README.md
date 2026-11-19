# How to Collect eBay Listing Data with Python and Export It to CSV

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-offline-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A small, fixture-first Python project for turning public eBay search listings into clean JSON or CSV records. It focuses on transparent parsing, reproducible tests, export, and explicit stop states—not on concealing automation or defeating access controls.

## Data fields

- item ID
- listing title
- displayed price
- condition
- shipping text
- seller summary
- listing URL

The included HTML is synthetic, so the complete example and test suite run without sending a request to eBay.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .

ebay-listing-data \
  --fixture fixtures/ebay-search.html \
  --format csv \
  --output sample-output/listings.csv
```

Expected result: `Exported 2 listings to sample-output/listings.csv`.

For JSON, replace `csv` with `json` and use `sample-output/listings.json`.

## Example record

```json
{
  "item_id": "DEMO-1001",
  "title": "Demo Mechanical Keyboard",
  "price": "$79.99",
  "condition": "New",
  "shipping": "Free shipping",
  "seller": "demo_store (99.8%)",
  "url": "https://www.ebay.com/itm/DEMO-1001"
}
```

All sample listings and sellers are fictional.

## How it works

```text
HTML fixture or explicitly enabled live page
                    │
                    ▼
          access-state classifier
          ├─ public result page ──► parser ──► validation ──► JSON/CSV
          └─ verification/login ──► structured stop result
```

The parser reads listing cards, normalizes relative links, preserves displayed values, and skips incomplete cards without a title. A verification or login page produces a structured stop instead of empty data.

## Tests

```bash
python -m unittest discover -s tests -v
```

The offline suite covers normal extraction, missing optional fields, URL normalization, verification detection, JSON/CSV export, rate limits, and live-mode safety limits.

## Optional live mode

Live requests are disabled unless `--live` is provided. Before using it, review the target page's current terms, robots guidance, and applicable rules.

```bash
ebay-listing-data \
  --live \
  --url "https://www.ebay.com/sch/i.html?_nkw=mechanical+keyboard" \
  --delay 3 \
  --max-pages 1 \
  --format json \
  --output listings.json
```

Built-in limits:

- no more than five pages per invocation;
- at least two seconds between requests;
- no automatic retry after HTTP 429;
- login and verification checkpoints stop the run;
- access errors remain visible rather than becoming empty results.

Live markup can change. Passing fixture tests verifies the parser contract, not permanent compatibility with a third-party site.

## Structured stop result

```json
{
  "status": "verification_required",
  "checkpoint": "interactive_verification",
  "retryable": false,
  "manual_action_required": true
}
```

This project does not solve verification challenges, automate login, or hide access failures.

## Repository layout

```text
ebay-listing-data-python/
├── src/ebay_listing_data/
├── fixtures/
├── sample-output/
├── tests/
└── .github/workflows/test.yml
```

## Responsible use

Use this project only for public data, authorized testing, personal research, or other lawful purposes. Respect website terms, robots guidance, rate limits, copyright, privacy obligations, and applicable law. Do not collect private or sensitive data, automate account activity, or interfere with a service.

eBay is a trademark of eBay Inc. This independent educational project is not affiliated with or endorsed by eBay.

## FAQ

### Does it require an eBay account?

No. Fixtures and tests run offline, and the project does not automate account login.

### Does it solve verification challenges?

No. It reports the checkpoint and stops for human review.

### Can I add another public field?

Yes. Extend `ListingRecord`, update the parser, add a synthetic fixture, and cover the field with an offline test.
