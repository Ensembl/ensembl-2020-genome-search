from flask import Flask
import os, json, sys
from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Indexer
from configs.config import get_config


app = Flask(__name__)
app.config.update(get_config())

if os.path.isfile(app.config['INDEX_FILE']):
    print(app.config['INDEX_FILE'])
    with open(app.config['INDEX_FILE'], 'r') as index_file:
        indexes = json.load(index_file)
        app.indexer = Indexer(indexes)
else:
    sys.exit('Problem opening Index file:{}'.format(app.config['INDEX_FILE']))

if os.path.isfile(app.config['GENOME_STORE_FILE']):
    print(app.config['GENOME_STORE_FILE'])
    with open(app.config['GENOME_STORE_FILE'], "r") as genome_store_file:
        genome_store_data = json.load(genome_store_file)
        app.genome_store = GenomeStore(genome_store_data)
else:
    sys.exit('Problem opening Genome store file:{}'.format(app.config['GENOME_STORE_FILE']))


with app.app_context():
    from blueprints import genome_search
    app.register_blueprint(genome_search.search_bp, url_prefix='/genome_search')


print("Starting the server...")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8011)