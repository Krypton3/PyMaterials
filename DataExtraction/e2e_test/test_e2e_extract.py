import unittest
import csv
import os
from MarvelExtraction import extract


class TestExtractE2E(unittest.TestCase):
    def setUp(self):
        # Path for the test CSV file that will be created during the test
        self.test_file = 'test_marvel.csv'

    def tearDown(self):
        # Clean up by removing the test CSV file after the test completes
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_extract_e2e(self):
        # Run the extract function and have it write to the test CSV file
        extract(self.test_file)

        # Now open the test CSV file and verify its contents
        with open(self.test_file, mode='r') as csv_file:
            reader = csv.reader(csv_file)

            # Read the header row
            header = next(reader)
            self.assertEqual(header, ['movie_name', 'movie_year', 'movie_rating_type', 'movie_description', 'movie_keywords',
                                      'movie_genre', 'movie_actors', 'movie_rating_user', 'movie_rating', 'direction', 'writers',
                                      'storyline'])

            rows = list(reader)

            # Ensure that there are two rows written (for Iron Man and The Incredible Hulk)
            self.assertEqual(len(rows), 2)

            # Validate the first movie (Iron Man)
            self.assertEqual(rows[0][0], 'Iron Man')  # movie_name
            self.assertEqual(rows[0][1], '2008-05-02')  # movie_year
            self.assertEqual(rows[0][2], 'PG')  # movie_rating_type

            # Validate the second movie (The Incredible Hulk)
            self.assertEqual(rows[1][0], 'The Incredible Hulk')  # movie_name
            self.assertEqual(rows[1][1], '2008-06-13')  # movie_year
            self.assertEqual(rows[1][2], 'PG')  # movie_rating_type


if __name__ == '__main__':
    unittest.main()
