import os
import unittest
import xmlrunner
from unittest.mock import patch
import requests


class TestLiveSite(unittest.TestCase):

    @patch('requests.get')
    def test_live_site(self, mock_get):
        # Set up the environment variable
        site_url = 'https://py-materials.netlify.app'
        os.environ['SITE_URL'] = site_url

        # Configure the mock to return a response with status_code 200
        mock_response = mock_get.return_value
        mock_response.status_code = 200

        # Retrieve the site URL from the environment
        site_url_env = os.getenv('SITE_URL')
        self.assertIsNotNone(site_url_env, "SITE_URL environment variable not set!")

        # Call the site and check the response
        response = requests.get(site_url_env)
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")

    @patch('requests.get')
    def test_site_not_found(self, mock_get):
        # Set up the environment variable
        site_url = 'https://py-materials.netlify.app'
        os.environ['SITE_URL'] = site_url

        # Configure the mock to return a response with status_code 404
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # Retrieve the site URL from the environment
        site_url_env = os.getenv('SITE_URL')
        self.assertIsNotNone(site_url_env, "SITE_URL environment variable not set!")

        # Call the site and check the response
        response = requests.get(site_url_env)
        self.assertEqual(response.status_code, 404, f"Expected status code 404, but got {response.status_code}")


if __name__ == "__main__":
    with open('e2e-live-reports/results.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output), verbosity=2)
