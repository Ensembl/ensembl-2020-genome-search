from flask import Blueprint, jsonify, make_response
from flask import current_app as app
from flask_restful import Resource, Api


search_bp = Blueprint('genome_search', __name__)
api = Api(search_bp)


print(app.indexes)

class Default(Resource):
    def get(self, path=''):
        # Return 404 response status code with error message if user queries any endpoint other than species
        return make_response(jsonify({'error': 'No such endpoint'}), 404)


class Species(Resource):
    def get(self, species_query, division):
        response_payload = {}

        genome_keys = app.indexes.search(species_query.lower())

        if genome_keys is not None:
            response_payload = {genome_key: app.genome_store.get_genome(genome_key) for genome_key in genome_keys}

        return make_response(jsonify({'match': response_payload}), 200)



api.add_resource(Default, '/', '/<path:path>')
api.add_resource(Species, '/species/<string:species_query>/<string:division>')