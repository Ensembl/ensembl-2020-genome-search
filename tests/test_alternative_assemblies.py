import app
import unittest

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.base_url = '/api/alternative_assemblies/'


    def test_if_alternative_assemblies_works(self):

        print("\n\t*** Testing if alternative assemblies endpoint works ***")

        query = '?genome_id=homo_sapiens_GCA_000001405_27'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)

        print("\t*** Response code: {} ***".format(response.status_code))


    def test_without_genome_id(self):

        print("\n\t*** Testing bad request without genome id ***")

        response = self.app.get(self.base_url)

        print('\t*** Request: {} ***'.format(self.base_url))

        self.assertEqual(response.status_code, 400)

        print("\t*** Response code: {} ***".format(response.status_code))


    def test_with_invalid_genome_id(self):

        print("\n\t*** Testing bad request with invalid genome id ***")

        query = '?genome_id=homo_sapiens_GC'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 400)

        print("\t*** Response code: {} ***".format(response.status_code))


if __name__ == '__main__':
    unittest.main()