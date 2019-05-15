from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api
import os, json
from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Indexer
from configs.app_config import get_config



application = Flask(__name__)
application.config.update(get_config())
api = Api(application)


class Default(Resource):
    def get(self, path=''):
        # Return 404 response status code with error message if user queries any endpoint other than species
        return make_response(jsonify({'error': 'No such endpoint'}), 404)


class Species(Resource):
    def get(self, species_query, division):
        response_payload = {}

        genome_keys = indexer.search(species_query.lower())

        if genome_keys is not None:
            response_payload = {genome_key: genome_store.get_genome(genome_key) for genome_key in genome_keys}

        return make_response(jsonify({'match': response_payload}), 200)


api.add_resource(Default, '/', '/<path:path>')
api.add_resource(Species, '/species/<string:species_query>/<string:division>')



if os.path.isfile(application.config['INDEX_FILE']):
    print(application.config['INDEX_FILE'])
    with open(application.config['INDEX_FILE'], 'r') as index_file:
        indexes = json.load(index_file)
        indexer = Indexer(indexes)

if os.path.isfile(application.config['GENOME_STORE_FILE']):
    print(application.config['GENOME_STORE_FILE'])
    with open(application.config['GENOME_STORE_FILE'], "r") as genome_store_file:
        genome_store_data = json.load(genome_store_file)
        genome_store = GenomeStore(genome_store_data)
