"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import app
import unittest
import json

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.base_url = '/api/genome/'


    def test_if_genome_info_works(self):

        self.base_url += 'info/'

        print("\n\t*** Testing if genome/info endpoint works ***")

        query = '?genome_id=3704ceb1-948d-11ec-a39d-005056b38ce3'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)

        print("\t*** Response code: {} ***".format(response.status_code))


    def test_if_multiple_genome_info_works(self):

        self.base_url += 'info/'

        print("\n\t*** Testing if genome/info endpoint works with multiple genome ids ***")

        query = '?genome_id=3704ceb1-948d-11ec-a39d-005056b38ce3&genome_id=a73357ab-93e7-11ec-a39d-005056b38ce3&genome_id=3704ceb1-948d-11ec-a39d-005056b38ce3'
        response = self.app.get(self.base_url + query)

        print('\t*** Request: {} ***'.format(self.base_url + query))

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)

        self.assertEqual(len(response_data['genome_info']), 3)

        print("\t*** Response code: {} ***".format(response.status_code))


if __name__ == '__main__':
    unittest.main()