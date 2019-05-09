from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Tokenize, Indexer
import sys, os, json



data_files_path = os.getcwd() + '/data_files'
genome_store_file_path = data_files_path + '/genome_store.json'
index_file_path = data_files_path + '/index.json'

keys_to_index = ['common_name', 'scientific_name', 'subtype']



if os.path.exists(genome_store_file_path):
#    user_response = input('Indexing Genome store {}. Continue? Y/N:'.format(genome_store_file_path))
    if True: #user_response.lower().startswith("y"):
        with open(genome_store_file_path, "r") as genome_store_file:
            genome_store_data = json.load(genome_store_file)
            genome_store = GenomeStore(genome_store_data)
    else:
        sys.exit('OK, exiting script!')



if os.path.exists(index_file_path):
#    user_response = input('Append to existing indexes? Y/N:'.format(index_file_path))
    if True: #user_response.lower().startswith("y"):
        with open(index_file_path, 'r') as index_file:
            indexes = json.load(index_file)
            indexer = Indexer(indexes)
    else:
        sys.exit('OK, exiting script!')
else:
    os.makedirs(data_files_path, exist_ok=True)
    indexer = Indexer()


tokenize = Tokenize()

for genome_key, genome in genome_store.get_next_genome():
    print(genome_key, genome)
    tokens = []
    for key in keys_to_index:
        tokens.extend(tokenize.create_tokens(genome[key]))
    print(set(tokens))

    for token in tokens:
        indexer.add_to_index(token, genome_key)


with open(index_file_path, 'w') as write_file:
    json.dump(indexer.get_indexes(), write_file)




