import requests
import json
import urllib.parse as urlparse



#def parse_next_request_url(url):
#  parsed = urlparse.urlparse(url)
#print(urlparse.parse_qs(parsed.query)['def'])

def do_rest_request(**kwargs):
   
    "This funtion expects a full_url to query or in absence of which construct a full URL from doamin and endpoints" 


    if 'full_url' in kwargs:
       query_url = kwargs['full_url']
    elif 'domain' in kwargs:
       query_url = kwargs['domain'] + '/'
       if 'endpoint' in kwargs:
          query_url += kwargs['endpoint']
       if 'request_params' in kwargs:
          query_url = query_url + '?' + urlparse.urlencode(kwargs['request_params'])
    else:
       return

#    print(query_url)
    
    rest_response = requests.get(query_url, headers = {'content-type':'application/json'})

    if rest_response.status_code != 200:
       raise Exception('Cannot fetch species info: {}'.format(rest_response.status_code))
    
    response_data = json.loads(rest_response.text)
#    print(response_data)
    return response_data




fungi_params = {
          "division_name" : "EnsemblFungi",
          "ensembl_genomes_version" : 43,
          "expand" : 'data_release,assembly,organism,division',
          "format" : "json",
        }
 
response_data = do_rest_request(domain="http://test-metadata.ensembl.org", endpoint="genome", request_params = fungi_params)

while 'next' in response_data:
    print(response_data['next'])
    response_data = do_rest_request(full_url=response_data['next'])


#for species in response_data['results']:
#    print(json.dumps(species))
