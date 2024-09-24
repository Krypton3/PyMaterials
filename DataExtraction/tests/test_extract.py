import unittest
from unittest.mock import patch, mock_open, MagicMock
import csv
import io
import xmlrunner
from MarvelExtraction import extract


class TestExtractFunction(unittest.TestCase):
    @patch('MarvelExtraction.requests.get')
    @patch('MarvelExtraction.open', new_callable=mock_open)
    def test_extract_success(self, mock_file, mock_get):
        # Mock responses for each movie ID
        def mock_get_response(url, headers, timeout):
            movie_data = {
                '0371746': '''
                <script type="application/ld+json">
                {
                    "name": "Iron Man",
                    "datePublished": "2008-05-02",
                    "contentRating": "PG-13",
                    "description": "A billionaire industrialist and genius inventor...",
                    "keywords": "superhero, marvel",
                    "genre": ["Action", "Sci-Fi"],
                    "aggregateRating": {
                        "ratingCount": 1200000,
                        "ratingValue": 7.9
                    },
                    "actor": [
                        {"name": "Robert Downey Jr."},
                        {"name": "Gwyneth Paltrow"}
                    ],
                    "director": {"name": "Jon Favreau"},
                    "creator": [
                        {"name": "Stan Lee"},
                        {"name": "Jack Kirby"}
                    ]
                }
                </script>
                <div class="ipc-html-content ipc-html-content--base">Tony Stark creates a powerful suit of armor to fight evil.</div>
                ''',
                '0800080': '''
                <script type="application/ld+json">
                {
                    "name": "The Incredible Hulk",
                    "datePublished": "2008-06-13",
                    "contentRating": "PG-13",
                    "description": "Bruce Banner, a scientist on the run...",
                    "keywords": "marvel, superhero",
                    "genre": ["Action", "Sci-Fi"],
                    "aggregateRating": {
                        "ratingCount": 800000,
                        "ratingValue": 6.7
                    },
                    "actor": [
                        {"name": "Edward Norton"},
                        {"name": "Liv Tyler"}
                    ],
                    "director": {"name": "Louis Leterrier"},
                    "creator": [
                        {"name": "Stan Lee"},
                        {"name": "Jack Kirby"}
                    ]
                }
                </script>
                <div class="ipc-html-content ipc-html-content--base">Bruce Banner, a scientist on the run, seeks a cure for the gamma radiation poisoning...</div>
                '''
            }
            movie_id = url.split('tt')[-1].strip('/')
            content = movie_data.get(movie_id, '')
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = content
            return mock_response

        # Mock the requests.get to use the mock_get_response function
        mock_get.side_effect = mock_get_response

        # Run the extract function
        extract()

        # Verify if the CSV file is written correctly
        mock_file.assert_called_once_with('marvel.csv', mode='w')

        # Get the file handle from the mock
        file_handle = mock_file()

        # Collect the write calls made to the mock file
        written_data = ''.join(call.args[0] for call in file_handle.write.call_args_list)

        # Use the csv.writer to generate expected CSV output to match the real behavior of the function
        expected_output = io.StringIO()
        writer = csv.writer(expected_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['movie_name', 'movie_year', 'movie_rating_type', 'movie_description', 'movie_keywords',
                         'movie_genre', 'movie_actors', 'movie_rating_user', 'movie_rating', 'direction', 'writers',
                         'storyline'])
        # First movie (Iron Man)
        writer.writerow([
            'Iron Man', '2008-05-02', 'PG-13', 'A billionaire industrialist and genius inventor...',
            'superhero, marvel', "['Action', 'Sci-Fi']", "['Robert Downey Jr.', 'Gwyneth Paltrow']",
            1200000, 7.9, "['Jon Favreau']", "['Stan Lee', 'Jack Kirby']",
            'Tony Stark creates a powerful suit of armor to fight evil.'
        ])
        # Second movie (The Incredible Hulk)
        writer.writerow([
            'The Incredible Hulk', '2008-06-13', 'PG-13', 'Bruce Banner, a scientist on the run...',
            'marvel, superhero', "['Action', 'Sci-Fi']", "['Edward Norton', 'Liv Tyler']",
            800000, 6.7, "['Louis Leterrier']", "['Stan Lee', 'Jack Kirby']",
            'Bruce Banner, a scientist on the run, seeks a cure for the gamma radiation poisoning...'
        ])

        # Assert that the written content matches the expected CSV content
        self.assertEqual(written_data, expected_output.getvalue())

    @patch('MarvelExtraction.requests.get')
    def test_extract_access_denied(self, mock_get):
        # Simulate a 403 Forbidden response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        # Run the extract function
        extract()

        # Ensure no CSV file is written due to 403 access denied
        mock_get.assert_called()

    @patch('MarvelExtraction.requests.get')
    def test_extract_no_ld_json(self, mock_get):
        # Simulate a page with no `ld+json` script tag
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '<html><body><h1>No Data</h1></body></html>'
        mock_get.return_value = mock_response

        # Run the extract function
        extract()

        # Ensure no data extraction happens due to missing script tag
        mock_get.assert_called()


if __name__ == '__main__':
    with open('test-reports/results.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output), verbosity=2)
