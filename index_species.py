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

from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Tokenize, Indexer
import sys, os, json, argparse
from configs.config import get_config


###########################
#  Helper functions
###########################

def tokenize_genome(args):
    tokens = []
    tokenize = Tokenize()
    for key in config['KEYS_TO_INDEX']:
        tokens.extend(tokenize.create_tokens(genome[key]))
    return tokens


def index_tokens(genome_key, tokens):
    print("Indexing genome with genome store key: {}".format(genome_key))
    for token in tokens:
        indexer.add_to_index(token, genome_key)


#############################
# End of functions
#############################


config = get_config()

parser = argparse.ArgumentParser(
    description='Index the whole genome store or only the genomes from genome store whose ids are passed as argument')
parser.add_argument('--index_genome_store_ids', help='List of genome store ids of genomes to index', nargs='+')

args = parser.parse_args()

if os.path.exists(config['GENOME_STORE_FILE']):
    #user_response = input('Indexing Genome store: {}. Continue? Y/N:'.format(config['GENOME_STORE_FILE']))
    #if user_response.lower().startswith("y"):
    with open(config['GENOME_STORE_FILE'], "r") as genome_store_file:
        genome_store_data = json.load(genome_store_file)
        genome_store = GenomeStore(genome_store_data)
    #else:
    #    sys.exit('OK, exiting script!')
else:
    raise Exception('No Genome store present: {}'.format(config['GENOME_STORE_FILE']))

if os.path.exists(config['INDEX_FILE']):
    #user_response = input('Adding indexes to existing index file: {}. Continue? Y/N:'.format(config['INDEX_FILE']))
    #if user_response.lower().startswith("y"):
    with open(config['INDEX_FILE'], 'r') as index_file:
        indexes = json.load(index_file)
        indexer = Indexer(indexes)
    #else:
    #    sys.exit('OK, exiting script!')
else:
    os.makedirs(config['DATA_FILE_PATH'], exist_ok=True)
    indexer = Indexer()

if args.index_genome_store_ids:
    for genome_key in args.index_genome_store_ids:
        genome = genome_store.get_genome(genome_key)
        if genome is not None:
            tokens = tokenize_genome(genome)
            index_tokens(genome_key, tokens)
else:
    for genome_key, genome in genome_store.get_next_genome():
        tokens = tokenize_genome(genome)
        index_tokens(genome_key, tokens)

with open(config['INDEX_FILE'], 'w') as write_file:
    json.dump(indexer.get_indexes(), write_file)
