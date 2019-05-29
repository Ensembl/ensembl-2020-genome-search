from flask import Flask
import os, json, sys
from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Indexer
from configs.config import get_config


app = Flask(__name__)
app.config.update(get_config())


def open_data_file(file):
    try:
        with open(file, 'r') as fh:
            contents = json.load(fh)
    except FileNotFoundError as fnf_error:
        sys.exit("Could not find the file {}\nExiting".format(file))
    except IOError as ioe_error:
        sys.exit("Problem reading file {}\nExiting!".format(file))
    except Exception as e:
        print("Unexpected error occurred while handling data files.\nExiting!")
        raise
    else:
        return contents


app.indexes = Indexer(open_data_file(app.config['INDEX_FILE']))
app.genome_store = GenomeStore(open_data_file(app.config['GENOME_STORE_FILE']))


with app.app_context():
    from blueprints import genome_search
    app.register_blueprint(genome_search.search_bp, url_prefix='/genome_search')


print("Starting the server...")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8011)