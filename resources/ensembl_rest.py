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

import requests, urllib.parse as urlparse


class EnsemblRest(object):

    """ Simple REST class. Add/update code as it evolves"""

    def __init__(self):
        pass

    def do_rest_request(self, **kwargs):

        if 'url' not in kwargs:
            raise Exception('No URL provided')
        else:
            query_url = kwargs['url']

        if 'query_params' in kwargs:
            query_url = kwargs['url'] + '?' + urlparse.urlencode(kwargs['query_params'])

        if 'method' in kwargs and kwargs['method'] == 'POST':
            raise Exception('POST not supported yet')
        else:
            rest_response = self.__get(query_url)

        return rest_response

    def __get(self, url):
        print("Querying {}".format(url))
        rest_response = requests.get(url, headers={'content-type': 'application/json'})
        return rest_response





