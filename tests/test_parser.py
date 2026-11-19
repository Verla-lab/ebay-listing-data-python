from pathlib import Path
import unittest

from ebay_listing_data.parser import classify_access, parse_listings

FIXTURES = Path(__file__).parents[1] / "fixtures"


class ParserTests(unittest.TestCase):
    def test_parses_two_listings(self):
        html = (FIXTURES / "ebay-search.html").read_text(encoding="utf-8")
        listings = parse_listings(html)
        self.assertEqual(len(listings), 2)
        self.assertEqual(listings[0].item_id, "DEMO-1001")
        self.assertEqual(listings[0].price, "$79.99")
        self.assertEqual(listings[1].condition, "Open box")
        self.assertEqual(listings[0].seller, "demo_store (99.8%)")

    def test_normalizes_relative_url(self):
        html = (FIXTURES / "ebay-search.html").read_text(encoding="utf-8")
        listing = parse_listings(html)[0]
        self.assertEqual(listing.url, "https://www.ebay.com/itm/DEMO-1001")

    def test_optional_fields_can_be_missing(self):
        html = (
            '<article data-item-id="DEMO-X">'
            '<span data-field="title">Title only</span></article>'
        )
        listing = parse_listings(html)[0]
        self.assertIsNone(listing.price)
        self.assertIsNone(listing.condition)
        self.assertIsNone(listing.shipping)

    def test_detects_verification_page(self):
        html = (FIXTURES / "verification.html").read_text(encoding="utf-8")
        access = classify_access(html)
        self.assertEqual(access.status, "verification_required")
        self.assertTrue(access.manual_action_required)
        self.assertEqual(parse_listings(html), [])


if __name__ == "__main__":
    unittest.main()
