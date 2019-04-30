import requests
import json, os
import urllib.parse as urlparse
from resources.genome import Genome
from resources.token import Tokenization


############################
#  Helper functions
###########################


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


def prepare_dump_files(data, directory):
  "Parse the response data and create json data files"

  if 'results' not in data: return
  #if 'results' not in data: raise Exception('Cannot parse data')
  
  tokenization = Tokenization()
  
  for species_info in data['results']:
    species = Genome(**species_info)
    tokens  = tokenization.create_tokens(species.genome)
    for token in tokens:
      all_tokens.setdefault(token, []).append(species.genome)
#    print(all_tokens)  
    with open(directory+"/"+species.genome+".json", "w") as write_file:
     json.dump(species, write_file, default=convert_to_dict)


def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  """
  return obj.__dict__




###########################################

# End of functions

##########################################



params = {
          "division_name" : "EnsemblFungi",
          "ensembl_genomes_version" : 43,
          "expand" : 'data_release,assembly,organism,division',
          "format" : "json",
        }


# TODO: Change this. Dont use global variables
all_tokens = {}

# Create data direcrtory where all the json files are stored
try:
         data_files_path = os.getcwd()+'/'+params['division_name']
         os.makedirs(data_files_path, exist_ok=True)
except OSError:
         print("Creation of the directory {} failed".format(data_files_path))
else:
         print("Successfully created the directory {}".format(data_files_path))


response_data = do_rest_request(query_params = params)

prepare_dump_files(response_data, data_files_path)

while 'next' in response_data and response_data['next'] is not None:
    response_data = do_rest_request(full_url=response_data['next'])
    prepare_dump_files(response_data, data_files_path)

#print(all_tokens)


with open(data_files_path+'/tokens.json', 'w') as token_file:
  json.dump(all_tokens, token_file)



################################################

# End of species dump

################################################




