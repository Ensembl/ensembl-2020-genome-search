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
        grouped_genomes = {}

        genome_keys =self._get_genome_keys()

        for genome_key in genome_keys:
            genome = self._get_genome(genome_key)
            matched_locations = self._find_match_locations(genome)

            grouped_genomes = self._group_by_location(matched_locations, grouped_genomes)

        print(grouped_genomes)

        response = self._prepare_response(grouped_genomes)


        return make_response(jsonify({'match': response}), 200)


    def _get_genome_keys(self):


        # Get Genome keys for every word of use query
        all_genome_keys = []
        for query_word in self.query_words:
            genome_keys_of_query_word = app.indexes.search(query_word)
            if genome_keys_of_query_word is None:
                all_genome_keys.append(set())
            else:
                all_genome_keys.append(set(genome_keys_of_query_word))

        # Create a set of Genome keys which are common to all the words in a user query
        valid_genome_keys = set.intersection(*all_genome_keys)

        print(all_genome_keys)
        print(valid_genome_keys)

        return valid_genome_keys


    def _get_genome(self, genome_key):

        return app.genome_store.get_genome(genome_key)
        # genome = Genome(genome_store_genome)
        # genome.create_genome_from_gs_format()
        # genome.sanitize()


    def _find_match_locations(self, genome):

        group_and_location_summary = {}
        # is there a match in common name? get the coordinates
        for genome_key_to_index in app.config['KEYS_TO_INDEX']:
            genome_name_words = genome[genome_key_to_index].lower().split()
            group_and_location = {}
            for query_word in self.query_words:
                current_location = 0
                for nth_word in range(len(genome_name_words)):
                    if genome_name_words[nth_word][:len(query_word)] == query_word:
                        # print('******Match*******')
                        group_and_location.setdefault('match_in_words', set()).add(nth_word + 1)
                        group_and_location.setdefault('position_in_genome_name', {}).setdefault(query_word, []).append(current_location)

                    # +1 for white space
                    current_location = current_location + len(genome_name_words[nth_word]) + 1

            if any(group_and_location):
                group_and_location_summary.setdefault('matches', {}).update({genome_key_to_index: group_and_location})
                group_and_location_summary['full_info'] = genome

        # print(group_and_location_summary)
        return group_and_location_summary

    def _group_by_location(self, summary, ordered_genomes):

        print(summary)

        final_group = min(list(set.union(*[summary['matches'][key]['match_in_words'] for key in summary['matches']])))

        ordered_genomes.setdefault(final_group, []).append(summary)

        return ordered_genomes

        #print(final_group)


    def _prepare_response(self, grouped_genomes):

        final_response = {}

        for group_number, genomes in grouped_genomes.items():
            for genome in genomes:
                response = {}
                response['genome_id'] = genome['full_info']['genome_id']
                response['reference_genome_id'] = genome['full_info']['reference_genome_id']
                response['common_name'] = genome['full_info']['common_name']
                response['scientific_name'] = genome['full_info']['scientific_name']
                response['subtype'] = genome['full_info']['subtype']
                response['matched_substrings'] = {}

                for match_key, match_info in genome['matches'].items():
                    match_location = match_info['position_in_genome_name']

                    for query, matches in match_location.items():

                        print(match_info)
                        for match in matches:
                            a = {}
                            a['lenght'] = len(query)
                            a['offset'] = match
                            a['match'] = match_key
                            # a['query_word'] = query
                            response['matched_substrings'].setdefault(query, []).append(a)


                #response['matched_substrings'] = genome['full_info']

                final_response.setdefault(group_number, []).append(response)

        return final_response









api.add_resource(Search, '/genome')