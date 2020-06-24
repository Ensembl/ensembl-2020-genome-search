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