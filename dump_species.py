import requests
import json, os
import urllib.parse as urlparse



class Species(object):
    def __init__(self, **species_info):
       
        # Use dict get method so that we get None value instead of KeyError when a key is not found 
        self.genome           = species_info.get('organism', {}).get('name')
        self.common_name      = species_info.get('organism', {}).get('display_name')
        self.scientific_name  = species_info.get('organism', {}).get('scientific_name')
        self.url_name         = species_info.get('organism', {}).get('url_name')
        self.assembly         = species_info.get('assembly', {}).get('assembly_name')
        self.test             = species_info.get('test', {}).get('test')
        self.__process_strains_info(**species_info)


    def __process_strains_info(self,  **species_info):
      
        if species_info.get('organism', {}).get('strain') is None:
          self.is_strain      = True
          self.parent_species = species_info.get('organism', {}).get('scientific_name')
        else:
          self.is_strain      = False  
          self.parent_species = None 
    


class Tokenization(object):
     def __init__(self, **kwargs):

       self.char_translate = {'_':' ', '-':'', '(':' ', ')':' ', '[':' ', ']':' '} 
       self.min_token_length = 3

     def create_tokens(self, string):
#       print(string) 
       translation_table          = string.maketrans(self.char_translate)
       translated_string          = string.translate(translation_table)
       translated_string_splitted = translated_string.split(' ')
       leading_0s_removed         = list(map(lambda s: s.lstrip('0'), translated_string_splitted))
#       print(leading_0s_removed)
       edge_ngram_tokens = [] 
       for token in leading_0s_removed:
         for i in range(self.min_token_length, len(token) + 1):
#           print(token[:i])
           edge_ngram_tokens.append(token[:i])
       return edge_ngram_tokens 


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
    species = Species(**species_info)
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




