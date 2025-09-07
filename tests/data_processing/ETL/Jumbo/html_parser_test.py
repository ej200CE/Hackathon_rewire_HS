import unittest
import logging
from pathlib import Path
from shared.models import ProductRow
from data_processing.ETL.Jumbo.html_parser import JumboHTMLParser

class JumboParser_test(unittest.TestCase):


    def setUp(self):
        logging.disable(logging.CRITICAL)


    def tearDown(self):
        logging.disable(logging.NOTSET)


    def test_predefined_output(self):

        # Storing pre-made output
        desired_output = ProductRow(store_id=1, external_sku='666821POT', name='Amorelli Pistache Crème 190 g', 
                            category='ontbijt,-broodbeleg-en-bakproducten', unit_type='weight', unit_value=1000, 
                            unit_description='1 kilogram', description='Pistache crème', country_of_origin=None)

        # Get path to HTML file in same directory as this test
        test_dir = Path(__file__).parent
        html_file = test_dir / "amorelli-pistache-creme-190-g-666821POT.html"
        
        # Read the HTML content
        with open(html_file, "rb") as f:
            html_content = f.read()
        
        # Create parser and test
        tested_parser = JumboHTMLParser("dummy", "Jumbo/", "dummy")
        key = "Jumbo/ontbijt,-broodbeleg-en-bakproducten/amorelli-pistache-creme-190-g-666821POT.html"
        
        result = tested_parser.parse_html(html_content, key)
        actual_output = result["product"]
        
        # Assert all fields match
        self.assertEqual(actual_output.store_id, desired_output.store_id)
        self.assertEqual(actual_output.external_sku, desired_output.external_sku)
        self.assertEqual(actual_output.name, desired_output.name)
        self.assertEqual(actual_output.category, desired_output.category)
        self.assertEqual(actual_output.unit_type, desired_output.unit_type)
        self.assertEqual(actual_output.unit_value, desired_output.unit_value)
        self.assertEqual(actual_output.unit_description, desired_output.unit_description)
        self.assertEqual(actual_output.description, desired_output.description)
        self.assertEqual(actual_output.country_of_origin, desired_output.country_of_origin)


    def run_all(self):
        self.test_predefined_output()


if __name__ == "__main__":
    tester = JumboParser_test()
    tester.test_input_output()
