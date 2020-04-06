import app
import unittest
import json

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.base_url = '/api/object/'


    def test_if_object_info_works(self):

        self.base_url += 'info/'

        print("\n\t*** Testing if object/info endpoint works ***")

        query = '?genome_id=homo_sapiens_GCA_000001405_27&object_id=gene:ENSG00000139618'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)

        print("\t*** Response code: {} ***".format(response.status_code))


    def test_if_track_list_work(self):

        self.base_url += 'track_list/'

        print("\n\t*** Testing if object/track_list endpoint works ***")

        query = '?genome_id=homo_sapiens_GCA_000001405_27&object_id=gene:ENSG00000139618'

        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)

        print("\t*** Response code: {} ***".format(response.status_code))


if __name__ == '__main__':
    unittest.main()