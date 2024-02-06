import unittest
import json
from core.ai import validate_catalogue

class TestCatalogueValidation(unittest.TestCase):
    def setUp(self):
        # Load test requirements
        with open('test_requirements.json', 'r') as file:
            self.test_requirements = json.load(file)
        # Load expected outcomes
        with open('expected_outcomes.json', 'r') as file:
            self.expected_outcomes = json.load(file)
        self.test_catalogue = 'path/to/test_catalogue.csv'

    def test_requirement_validation(self):
        for test_case in self.test_requirements:
            buyer_name = test_case['buyer_name']
            requirements = test_case['requirements']
            
            # Fetch the expected outcomes for the current buyer_name
            expected = self.expected_outcomes[buyer_name]['expected_outcomes']
            
            # Validate each requirement
            for requirement, expected_outcome in zip(requirements, expected):
                result = validate_catalogue(self.test_catalogue, [requirement])
                result_json = json.loads(result)
                
                # Extract the expected values for comparison
                expected_passed = expected_outcome['passed']
                expected_failed_rows = expected_outcome['rows_failed']
                
                # Assertions
                self.assertEqual(result_json['passed'], expected_passed, f"Pass/fail status did not match expected for requirement: {requirement}")
                self.assertListEqual(sorted(result_json['rows_failed']), sorted(expected_failed_rows), f"Failed rows do not match expected for requirement: {requirement}")

    # Additional tests as necessary

if __name__ == '__main__':
    unittest.main()
