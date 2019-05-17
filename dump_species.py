import requests, json, os, sys, argparse
import urllib.parse as urlparse
from resources.genome import Genome
from resources.genome_store import GenomeStore
from configs.config import get_config


############################
#  Helper functions
###########################


def do_rest_request(**kwargs):
    """This function expects full_url or in absence of which, expects a combination of "url" and "query_params"""

    if 'full_url' in kwargs:
        query_url = kwargs['full_url']
    elif 'rest_url' in kwargs and 'query_params' in kwargs:
        query_url = kwargs['url'] + '?' + urlparse.urlencode(kwargs['query_params'])
    else:
        raise Exception('Provide either "full_url" or a combination of "url" and "query_params"')

    print("Querying {}".format(query_url))
    rest_response = requests.get(query_url, headers={'content-type': 'application/json'})

    if rest_response.status_code != 200:
        raise Exception('Cannot fetch info: {}'.format(rest_response.status_code))

    rest_response = json.loads(rest_response.text)

    return rest_response


def prepare_genome_store(params, source='metadata_registry'):
    if source == 'metadata_registry':
        full_url = config['METADATA_REGISTRY_URL'] + '?' + urlparse.urlencode(params)
        prepare_gs_from_metadata_registry(full_url)
    elif source == 'custom_genome_files':
        genome_file_dir = params['<path>']
        prepare_gs_from_raw_files(genome_file_dir)
    elif source == 'something_else':
        pass
    else:
        pass


def prepare_gs_from_metadata_registry(url):
    response_from_metadata = do_rest_request(full_url=url)

    if 'results' not in response_from_metadata:
        raise Exception('Cannot parse data. Invalid format')

    for metadata_genome in response_from_metadata['results']:

        genome = Genome(metadata_genome)
        genome.create_genome_from_metadata()
        genome.sanitize()

        genome_store.add_to_genome_store(genome)

    if 'next' in response_from_metadata and response_from_metadata['next'] is not None:
        prepare_gs_from_metadata_registry(response_from_metadata['next'])


def prepare_gs_from_raw_files(dir):
    pass


###########################################

# End of functions

##########################################




config = get_config()

parser = argparse.ArgumentParser(description='Create Genome Store to use with Species selector')
parser.add_argument('--fetch_by_genome', help='Create/Update Genome store with genomes', nargs='+')
parser.add_argument('--fetch_by_division', help='Create/Update Genome store with genomes from Ensembl divisions', nargs='+')
parser.add_argument('--create_from_file', help='Create/Update Genome store with genomes from a file')

args = parser.parse_args()


# Override default value in config if there is at least one relevant cli argument provided while running the script
if any(vars(args).values()):
    for arg_key, arg_value in vars(args).items():
            config[arg_key.upper()] = arg_value


print(config)

if os.path.exists(config['GENOME_STORE_FILE']):
    user_response = input(
        'Appending to existing Genome store at {}. Continue? Y/N:'.format(config['GENOME_STORE_FILE']))
    if user_response.lower().startswith("y"):
        with open(config['GENOME_STORE_FILE'], "r") as genome_store_file:
            genome_store_data = json.load(genome_store_file)
            genome_store = GenomeStore(genome_store_data)
    else:
        sys.exit('OK, exiting script!')
else:
    os.makedirs(config['DATA_FILE_PATH'], exist_ok=True)
    genome_store = GenomeStore()

req_params = {
    "expand": 'data_release,assembly,organism,division',
    "format": "json",
}

# Prepare query params to get data
req_params.update({"ensembl_version": config['V_VERSION']})

if 'FETCH_BY_DIVISION' in config and config['FETCH_BY_DIVISION'] is not None:
    for division in config['FETCH_BY_DIVISION']:
        if division in config['VALID_DIVISIONS'].keys() or division in config['VALID_DIVISIONS'].values():
            req_params.update({'division_name': division})
            print('Fetching data for division {} and release {}'.format(division, req_params['ensembl_version']))
            prepare_genome_store(req_params, 'metadata_registry')
        else:
            sys.exit('Invalid division {}.\nUse divisions from list: {}'.format(division, list(config['VALID_DIVISIONS'].values())))
elif 'FETCH_BY_GENOME' in config and config['FETCH_BY_GENOME'] is not None:
    for genome in config['FETCH_BY_GENOME']:
        req_params.update({'organism_name': genome})
        print('Fetching data for species {} and release {}'.format(genome, req_params['ensembl_version']))
        prepare_genome_store(req_params, 'metadata_registry')
else:
    sys.exit('Division/Genome/File not provided. Exiting!')



with open(config['GENOME_STORE_FILE'], "w") as write_file:
    json.dump(genome_store.get_genome_store(), write_file)

################################################

# End of species dump

################################################
