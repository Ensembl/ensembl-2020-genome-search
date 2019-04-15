import requests
import json, os
import urllib.parse as urlparse



def do_rest_request(rest_endpoint='http://test-metadata.ensembl.org/genome', query_params={"format" : "json"}, **kwargs):
   
    "This funtion expects a full_url to query or in absence of which construct a full URL from domain and endpoints" 

    if 'full_url' in kwargs:
       query_url = kwargs['full_url']
    else: 
       query_url = rest_endpoint + '?' + urlparse.urlencode(query_params)

    print("Querying {}".format(query_url))

    rest_response = requests.get(query_url, headers = {'content-type':'application/json'})

    if rest_response.status_code != 200:
       raise Exception('Cannot fetch info: {}'.format(rest_response.status_code))
    
    response_data = json.loads(rest_response.text)

    return response_data


def create_json_files(data):
  "Parse the response data and create json data files"

  if 'results' not in data: return
  #if 'results' not in data: raise Exception('Cannot parse data')

  for species_info in data['results']:
    with open("data/"+species_info['organism']['name']+".json", "w") as write_file:
     json.dump(species_info, write_file)




# Create data direcrtory where all the json files are stored
try:
         data_files_path = os.getcwd()+"/data"
         os.makedirs(data_files_path, exist_ok=True)
except OSError:
         print("Creation of the directory {} failed".format(data_files_path))
else:
         print("Successfully created the directory {}".format(data_files_path))


fungi_params = {
          "division_name" : "EnsemblFungi",
          "ensembl_genomes_version" : 43,
          "expand" : 'data_release,assembly,organism,division',
          "format" : "json",
        }
 
response_data = do_rest_request(query_params = fungi_params)

create_json_files(response_data)

while 'next' in response_data and response_data['next'] is not None:
    response_data = do_rest_request(full_url=response_data['next'])
    create_json_files(response_data)

