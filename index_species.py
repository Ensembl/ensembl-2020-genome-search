from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Tokenize, Indexer
import sys, os, json
from configs.config import get_config



config = get_config()


if os.path.exists(config['GENOME_STORE_FILE']):
    user_response = input('Indexing Genome store {}. Continue? Y/N:'.format(config['GENOME_STORE_FILE']))
    if user_response.lower().startswith("y"):
        with open(config['GENOME_STORE_FILE'], "r") as genome_store_file:
            genome_store_data = json.load(genome_store_file)
            genome_store = GenomeStore(genome_store_data)
    else:
        sys.exit('OK, exiting script!')
else:
    raise Exception('No Genome store present: {}'.format(config['GENOME_STORE_FILE']))



if os.path.exists(config['INDEX_FILE']):
    user_response = input('Append to existing indexes? Y/N:'.format(config['INDEX_FILE']))
    if user_response.lower().startswith("y"):
        with open(config['INDEX_FILE'], 'r') as index_file:
            indexes = json.load(index_file)
            indexer = Indexer(indexes)
    else:
        sys.exit('OK, exiting script!')
else:
    os.makedirs(config['DATA_FILE_PATH'], exist_ok=True)
    indexer = Indexer()


tokenize = Tokenize()

for genome_key, genome in genome_store.get_next_genome():
    print(genome_key, genome)
    tokens = []
    for key in config['KEYS_TO_INDEX']:
        tokens.extend(tokenize.create_tokens(genome[key]))
    print(set(tokens))

    for token in tokens:
        indexer.add_to_index(token, genome_key)


with open(config['INDEX_FILE'], 'w') as write_file:
    json.dump(indexer.get_indexes(), write_file)