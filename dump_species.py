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
        url = config['METADATA_REGISTRY_URL'] + '?' + urlparse.urlencode(params)
        response_from_metadata = do_rest_request(full_url=url)
        prepare_gs_from_mr_format(response_from_metadata)
    elif source == 'custom_genome_file':
        genome_file_path = params['file']
        if os.path.exists(genome_file_path):
            with open(genome_file_path, "r") as genome_file_fn:
                custom_genome_data = json.load(genome_file_fn)
            prepare_gs_from_mr_format(custom_genome_data)
        else:
            sys.exit('Problem opening custom genome file:{}'.format(genome_file_path))
    elif source == 'something_else':
        pass
    else:
        pass


def prepare_gs_from_mr_format(metadata_registry_data):
    if 'results' not in metadata_registry_data:
        raise Exception('Cannot parse data. Invalid format')

    for metadata_genome in metadata_registry_data['results']:
        if metadata_genome['organism']['name'] == 'escherichia_coli_str_k_12_substr_mg1655':
            metadata_genome['organism']['name'] = 'escherichia_coli_str_k_12_substr_mg1655_gca_000005845'
        genome = Genome(metadata_genome)
        genome.create_genome_from_mr_format()
        genome.sanitize()
        genome_store.add_to_genome_store(genome)
    if 'next' in metadata_registry_data and metadata_registry_data['next'] is not None:
        response_from_metadata = do_rest_request(full_url=metadata_registry_data['next'])
        prepare_gs_from_mr_format(response_from_metadata)


###########################################

# End of functions

##########################################


config = get_config()

parser = argparse.ArgumentParser(description='Create Genome Store to use with Species selector')
parser.add_argument('--fetch_by_genome', help='Create/Update Genome store with genomes', nargs='+')
parser.add_argument('--fetch_by_division', help='Create/Update Genome store with genomes from Ensembl divisions',
                    nargs='+')
parser.add_argument('--create_from_file', help='Create/Update Genome store with genomes from a custom file')
parser.add_argument('--return_genome_store_ids', help='Return added/updated Genome store ids to use with indexer',
                    nargs='?', const=True, default=False)

args = parser.parse_args()

sys.setrecursionlimit(10000)

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
    "expand": 'assembly, organism, division',
    "format": "json",
}

# Prepare query params to get data
req_params.update({"ensembl_version": config['V_VERSION']})

if args.fetch_by_genome is not None:
    for genome in args.fetch_by_genome:
        req_params.update({'organism_name': genome, 'exact_match': 'true'})
        print('Fetching data for species {} and release {}'.format(genome, req_params['ensembl_version']))
        prepare_genome_store(req_params, 'metadata_registry')
elif args.fetch_by_division is not None:
    for division in args.fetch_by_division:
        if division in config['VALID_DIVISIONS'].keys() or division in config['VALID_DIVISIONS'].values():
            req_params.update({'division_name': division})
            print('Fetching data for division {} and release {}'.format(division, req_params['ensembl_version']))
            prepare_genome_store(req_params, 'metadata_registry')
        else:
            sys.exit('Invalid division {}.\nUse divisions from list: {}'.format(division, list(
                config['VALID_DIVISIONS'].values())))
elif args.create_from_file is not None:
    req_params.update({'file': args.create_from_file})
    prepare_genome_store(req_params, 'custom_genome_file')
else:
    parser.print_help()
    sys.exit()

with open(config['GENOME_STORE_FILE'], "w") as write_file:
    json.dump(genome_store.get_genome_store(), write_file)

if args.return_genome_store_ids and genome_store.processed_genomes_list:
    print("\n\n***Run the indexing script as below:***\n\n python index_species.py --index_genome_store_ids {}".format(
        ' '.join(str(genome_key) for genome_key in genome_store.processed_genomes_list)))

################################################

# End of species dump

################################################
