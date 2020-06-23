#
#    See the NOTICE file distributed with this work for additional information
#    regarding copyright ownership.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
import app
import unittest
import json

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.base_url = '/api/genome_search/'


    def test_if_search_works(self):

        print("\n\t*** Testing if search endpoint works ***")

        query = '?query=musc'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)

        print("\t*** Response code: {} ***".format(response.status_code))


    def test_without_query_word(self):

        print("\n\t*** Testing bad request without query word ***")

        response = self.app.get(self.base_url)

        print('\t*** Request: {} ***'.format(self.base_url))

        self.assertEqual(response.status_code, 400)

        print("\t*** Response code: {} ***".format(response.status_code))


    def test_two_human_assemblies(self):

        print("\n\t*** Testing if there are two assemblies for Homo sapiens ***")

        query = '?query=homo sapiens'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        print("\t*** Response code: {} ***".format(response.status_code))
        #print("\t*** Response data: {} ***".format(response_data))

        self.assertEqual(len(response_data['genome_matches'][0]), 2)

    # Current 7 species does not have grouping but 45k species has it
    # Generating genome_store and indexing it for 45k species takes 1 hour
    # Once we have faster process for genome_store generation enable this test

    # def test_search_grouping(self):

    #     print("\n\t*** Testing if search hits grouping is working ***")

    #     query = '?query=human'
    #     response = self.app.get(self.base_url + query)
    #     print(response_data)

    #     print('\t*** Request: {} ***'.format(self.base_url + query))

    #     self.assertEqual(response.status_code, 200)
    #     response_data = json.loads(response.data)

    #     print("\t*** Response code: {} ***".format(response.status_code))
    #     #print("\t*** Response data: {} ***".format(response_data))

    #     self.assertGreater(len(response_data['genome_matches']), 1)


if __name__ == '__main__':
    unittest.main()