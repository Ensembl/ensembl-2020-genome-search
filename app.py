from flask import Flask, jsonify, make_response
import json
import re
from flask_restful import Resource, Api
import os

application = Flask(__name__)
api = Api(application)


class Default(Resource):
   def get(self, path=''):
       # Return 404 response status code with error message if user queries any endpoint other than species
       return make_response(jsonify({'error': 'No such endpoint'}), 404)

class Species(Resource):
   def get(self, species_query, division):
     
      tokens_file_path = "{}/Ensembl{}/tokens.json".format(os.getcwd(), division.capitalize())
      all_species_json = []
      print(tokens_file_path)
      if os.path.isfile(tokens_file_path):
         print(tokens_file_path) 
         with open(tokens_file_path, 'r') as tokens_file:
            tokens = json.load(tokens_file)
        
         species_list = tokens.get(species_query.lower())

         if species_list is not None:
            for species in species_list:
                with open("{}/Ensembl{}/{}.json".format(os.getcwd(),division.capitalize(), species.lower()), 'r') as species_file:
                  species_data = json.load(species_file)
                  all_species_json.append(species_data) 
            return make_response(jsonify({'match': all_species_json}), 200) 
         else: 
            return make_response(jsonify({'info': 'No species starting with {}'.format(species_query)}), 400)
      else: 
         return make_response(jsonify({'info': 'Invalid division'}), 400)

api.add_resource(Default, '/', '/<path:path>')
api.add_resource(Species, '/species/<string:species_query>/<string:division>')


if __name__ == "__main__":
	application.run(debug=True, host="0.0.0.0", port="8011")
