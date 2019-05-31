from flask import Flask, make_response, jsonify
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

    # TODO: errorhandlers listening to only 404 errors at the moment. Needs investigating.
    register_generic_error_handlers(application)

    return application



def register_generic_error_handlers(application):

    @application.errorhandler(404)
    def not_found(error):
        #print('4040404040404')
        return make_response(jsonify({'error': 'Not found'}), 404)

    @application.errorhandler(405)
    def not_found(error):
        return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

    @application.errorhandler(500)
    def internal_error(error):
        #print('500500500500')
        return make_response(jsonify({'message': 'Internal Server Errorsss'}), 500)


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

#### use gunicorn app:app --workers 2 --preload
# app = create_app()
# print(app.error_handler_spec)

if __name__ == "__main__":
    app = create_app()
    #print(app.error_handler_spec)
    app.run(host="0.0.0.0", port=8011)
