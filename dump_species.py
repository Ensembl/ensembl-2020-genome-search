import requests, json, os, sys
import urllib.parse as urlparse
from resources.genome import Genome
from resources.genome_store import GenomeStore


############################
#  Helper functions
###########################


def do_rest_request(rest_endpoint='http://test-metadata.ensembl.org/genome', query_params={"format": "json"}, **kwargs):
    """This function expects a full_url to query or in absence of which construct a full URL from domain and endpoints"""

    if 'full_url' in kwargs:
        query_url = kwargs['full_url']
    else:
        query_url = rest_endpoint + '?' + urlparse.urlencode(query_params)

    print("Querying {}".format(query_url))
    rest_response = requests.get(query_url, headers={'content-type': 'application/json'})

    if rest_response.status_code != 200:
        raise Exception('Cannot fetch info: {}'.format(rest_response.status_code))

    rest_response = json.loads(rest_response.text)

    return rest_response


def add_to_genome_store(data, genome_store):
    """Parse the response data and create json data files"""

    if 'results' not in data:
        raise Exception('Cannot parse data. Invalid format')

    genome_key = genome_store.get_max_key()

    for genome_info in data['results']:

        genome = Genome(genome_info)
        genome.sanitize()

        #print(genome.common_name, genome.genome_id)

        genome_key += 1
        genome_store.add_to_store(genome_key, convert_to_dict(genome))


def convert_to_dict(obj):
    """ A function takes in a custom object and returns a dictionary representation of the object."""
    return obj.__dict__


###########################################

# End of functions

##########################################


data_files_path = os.getcwd() + '/data_files'
genome_store_file_path = data_files_path + '/genome_store.json'

if os.path.exists(genome_store_file_path):
    user_response = input('Appending to existing Genome store at {}. Continue? Y/N:'.format(genome_store_file_path))
    if user_response.lower().startswith("y"):
        with open(genome_store_file_path, "r") as genome_store_file:
            genome_store_data = json.load(genome_store_file)
            genome_store = GenomeStore(genome_store_data)
    else:
        sys.exit('OK, exiting script!')
else:
    os.makedirs(data_files_path, exist_ok=False)
    genome_store = GenomeStore()






params = {
    "division_name": "EnsemblFungi",
    "ensembl_genomes_version": 43,
    "expand": 'data_release,assembly,organism,division',
    "format": "json",
}



response_data = do_rest_request(query_params=params)
add_to_genome_store(response_data, genome_store)

while 'next' in response_data and response_data['next'] is not None:
    response_data = do_rest_request(full_url=response_data['next'])
    add_to_genome_store(response_data, genome_store)

with open(genome_store_file_path, "w") as write_file:
    json.dump(genome_store.get_genome_store(), write_file, default=convert_to_dict)

################################################

# End of species dump

################################################
