from flask import Flask
import os, json, sys
from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Indexer
from configs.config import get_config


def create_app():
    application = Flask(__name__)
    application.config.update(get_config())

    application.indexes = Indexer(open_data_file(application.config['INDEX_FILE']))
    print("Loaded indexes")
    application.genome_store = GenomeStore(open_data_file(application.config['GENOME_STORE_FILE']))
    print("Loaded Genome store")

    with application.app_context():
        from blueprints import genome_search
        application.register_blueprint(genome_search.search_bp, url_prefix='/genome_search')

    return application


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









print("Starting the server...")

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8011)