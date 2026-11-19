import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ebay_listing_data.exporter import export_csv, export_json
from ebay_listing_data.models import ListingRecord


class ExporterTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            ListingRecord(
                "DEMO-TEST",
                "Test listing",
                "$10.00",
                "Used",
                "Free shipping",
                "test_seller (100%)",
                "https://example.test",
            )
        ]

    def test_json_export(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "listings.json"
            export_json(self.records, path)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data[0]["title"], "Test listing")

    def test_csv_export(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "listings.csv"
            export_csv(self.records, path)
            with path.open(encoding="utf-8") as handle:
                data = list(csv.DictReader(handle))
            self.assertEqual(data[0]["item_id"], "DEMO-TEST")


if __name__ == "__main__":
    unittest.main()
