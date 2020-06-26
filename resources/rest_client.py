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
import json

class EnsemblREST(object):

    """REST Client for ensembl rest"""

    def __init__(self):
        self.base_url = 'https://rest.ensembl.org'

    def do_get(self, url, **kwargs):
        json_data = {}
        response = requests.get(url,headers={'content-type': 'application/json'})
        if response.status_code == 200:
            json_data = response.json()

        return json_data

    def get_assembly_info(self, spname, **kwargs):
        # info/assembly/homo_sapiens?content-type=application/json;bands=1
        url = "{}/info/assembly/{}".format(self.base_url, spname)
        json_data = self.do_get(url) 
        return json_data

    def get_region_info(self, spname, rname, **kwargs):
        # http://rest.ensembl.org/info/assembly/homo_sapiens/X?content-type=application/json
        url = "{}/info/assembly/{}/{}".format(self.base_url, spname, rname, **kwargs)
        json_data = self.do_get(url)
        return json_data

class EnsemblGRCH37REST(object):

    """REST Client for grch37 ensembl rest"""

    def __init__(self):
        self.base_url = 'https://grch37.rest.ensembl.org'

    def do_get(self, url, **kwargs):
        json_data = {}
        response = requests.get(url,headers={'content-type': 'application/json'})
        if response.status_code == 200:
            json_data = response.json()

        return json_data

    def get_assembly_info(self, spname, **kwargs):
        # info/assembly/homo_sapiens?content-type=application/json;bands=1
        url = "{}/info/assembly/{}".format(self.base_url, spname)
        json_data = self.do_get(url) 
        return json_data

    def get_region_info(self, spname, rname, **kwargs):
        # http://rest.ensembl.org/info/assembly/homo_sapiens/X?content-type=application/json
        url = "{}/info/assembly/{}/{}".format(self.base_url, spname, rname)
        json_data = self.do_get(url)
        return json_data