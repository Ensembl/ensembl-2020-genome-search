from flask import Blueprint, jsonify, make_response, abort, request
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
import re
from resources.genome import Genome


search_bp = Blueprint('genome_search', __name__)
api = Api(search_bp)


# print(app.indexes)


class Search(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('query',  type=str, required=True, help="Missing 'query' param in the request.")
        parser.add_argument('filter', type=str, default='all_divisions')

        self.args = parser.parse_args()

        # Split user query to work on each word
        self.query_words = self.args.query.split()

        # print(args)

        response_payload = {}

        genome_keys =self._get_genome_keys()

        genomes = self._get_genomes(genome_keys)


        for genome in genomes:
            group = self._get_group_and_location(genome)


        # return make_response(jsonify({'match': genomes}), 200)

    def _get_genome_keys(self):


        # Get Genome keys for every word of use query
        all_genome_keys = []
        for query_word in self.query_words:
            genome_keys_of_query_word = app.indexes.search(query_word)
            if genome_keys_of_query_word is None:
                all_genome_keys.append(set())
            else:
                all_genome_keys.append(set(genome_keys_of_query_word))

        # Create a set of Genome keys which are common to all the words in user query
        valid_genome_keys = set.intersection(*all_genome_keys)

        print(all_genome_keys)
        print(valid_genome_keys)

        return valid_genome_keys


    def _get_genomes(self, genome_keys):

        genomes = []
        for genome_key in genome_keys:
            genome_store_genome = app.genome_store.get_genome(genome_key)
            # genome = Genome(genome_store_genome)
            # genome.create_genome_from_gs_format()
            # genome.sanitize()

            genomes.append(genome_store_genome)

        return genomes

    def _get_group_and_location(self, genome):

        # is there a match in common name? get the coordinates
        for key_to_index in app.config['KEYS_TO_INDEX']:
            # space_match = [m for m in re.finditer(' ', genome[key_to_index])]

            genome_name_words = genome[key_to_index].lower().split()

            for query_word in self.query_words:
                current_location = 0
                for nth_word in range(len(genome_name_words)):
                    group = 0
                    if genome_name_words[nth_word][0:len(query_word)] == query_word:
                        group = nth_word
                        print('******Match*******')
                    current_location = current_location + 1
                    print("{}----{}----{}----{}".format(group, current_location, query_word, ' '.join(genome_name_words)))
                    current_location = current_location + len(genome_name_words[nth_word])

                # if query_word in genome[key_to_index]:
                #
                # position = genome[key_to_index].find(query_word)
                # print(position)
                # print("{}----{}----- {}".format(genome[key_to_index], query_word, position))




        # is there a match in sci name? get the coordinates
        # is there a match in assembly name? get the coordinates












api.add_resource(Search, '/genome')