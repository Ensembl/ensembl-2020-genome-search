import requests
import json
import urllib.parse as urlparse



def parse_next_request_url(url):
  parsed = urlparse.urlparse(url)
print(urlparse.parse_qs(parsed.query)['def'])

def do_rest_request(domain, endpoint, request_params):
   
    "This funtion expects a full URL to query or in absence of which construct a full URL from doamin and endpoints"
 
    url = domain+'/'+endpoint+'/'
    
#    print(url)
#    print(request_params)
    
    rest_response = requests.get(url, params = request_params, headers = {'content-type':'application/json'})

    if rest_response.status_code != 200:
       raise Exception('Cannot fetch species info: {}'.format(rest_response.status_code))
    
    response_data = json.loads(rest_response.text)
#    print(response_data)
    return response_data





domain = "http://test-metadata.ensembl.org"
endpoint = "genome"
request_params = {
          "division_name" : "EnsemblFungi",
          "ensembl_genomes_version" : 43,
          "expand" : 'data_release,assembly,organism,division',
          "format" : "json",
        }
 
response_data = do_rest_request(domain, endpoint, request_params)

while 'next' in response_data:
    print(response_data['next'])
    parse_next_request_url(response_data['next'])
    response_data = do_rest_request(domain, endpoint, request_params)


#for species in response_data['results']:
#    print(json.dumps(species))
