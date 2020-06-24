"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from flask import Blueprint, jsonify, make_response, abort, request
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
from resources.ensembl_indexer import Tokenize


search_bp = Blueprint('genome_search', __name__)
api = Api(search_bp)


class Search(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('query',  type=str, required=True, help="Missing 'query' param in the request.", location='args')
        parser.add_argument('division', type=str, location='args')
        parser.add_argument('exclude', type=str, location='args', action='append')
        parser.add_argument('limit', type=int, location='args')


        self.args = parser.parse_args()
        # print(self.args)

        tokenize = Tokenize()
        self.tokens  = tokenize.create_tokens(self.args.query)

        # Split user query to work on each word
        self.query_words = self.args.query.split()

        grouped_by_match_position = {}
        total_matches = 0

        genome_keys = self._get_genome_keys()

        for genome_key in genome_keys:
            genome = self._get_genome(genome_key)

            # Skip if genome search hit does not belong to user supplied division
            if self.args.division is not None:
                if not self._check_if_belongs_to_division(genome):
                    continue

            # Skip if search hit is for a genome which is in exclusion list
            if self.args.exclude is not None:
                if self._check_if_in_exclude_list(genome):
                    continue

            matched_positions = self._locate_match_positions(genome)

            if any(matched_positions):
                grouped_by_match_position = self._group_by_match_position(grouped_by_match_position, matched_positions)
                total_matches += 1

        response = self._prepare_response(grouped_by_match_position, total_matches)

        return make_response(jsonify(response), 200)

    def _get_genome_keys(self):

        # Get Genome keys for every token in user query
        genome_keys = []
        for token in self.tokens:
            genome_keys_of_token = app.indexes.search(token)
            if genome_keys_of_token is None:
                genome_keys.append(set())
            else:
                genome_keys.append(set(genome_keys_of_token))

        # Create a set of Genome keys which are common to all the tokens in a user query
        if any(genome_keys):
            return set.intersection(*genome_keys)
        else:
            return set()

    def _get_genome(self, genome_key):
        return app.genome_store.get_genome(genome_key)

    def _check_if_belongs_to_division(self, genome):
        if self.args.division in [*app.config['VALID_DIVISIONS'].values()]:
            if self.args.division in genome['division']:
                return True
            else:
                return False
        else:
            return abort(400, {'error': 'Invalid division filter. Use values from {}'.format(', '.join([*app.config['VALID_DIVISIONS'].values()]))})

    def _check_if_in_exclude_list(self, genome):
        if genome.get('genome_id') in self.args.exclude:
            return True
        else:
            return False

    def _locate_match_positions(self, genome):

        genome_with_matched_positions = {}

        for genome_key_to_index in app.config['KEYS_TO_INDEX']:
            genome_name_words = genome[genome_key_to_index].split()
            match_positions = {}
            for query_word in self.query_words:
                current_location = 0
                for nth_word in range(len(genome_name_words)):
                    if query_word.lower() == genome_name_words[nth_word][:len(query_word)].lower():
                        # print('******Match*******')
                        match_positions.setdefault('match_in_nth_word', set()).add(nth_word + 1)
                        match_positions.setdefault('offsets', {})
                        if current_location not in match_positions['offsets'].keys() or \
                                match_positions['offsets'][current_location] < len(query_word):
                            match_positions['offsets'].update({current_location: len(query_word)})

                    # +1 for white space
                    current_location = current_location + len(genome_name_words[nth_word]) + 1

            if any(match_positions):
                genome_with_matched_positions.setdefault('matches_info', {}).update({genome_key_to_index: match_positions})
                genome_with_matched_positions['genome_info'] = genome

        return genome_with_matched_positions

    def _group_by_match_position(self, grouped_by_match_position, genome_with_matched_positions):

        group_number = min(list(set.union(*[match_info['match_in_nth_word'] for match_info in genome_with_matched_positions['matches_info'].values()])))
        grouped_by_match_position.setdefault(group_number, []).append(genome_with_matched_positions)

        return grouped_by_match_position

    def _prepare_response(self, grouped_genomes, total_matches):

        response = {}
        genome_hit_count = 0

        for group_number, genomes in sorted(grouped_genomes.items()):
            group = []
            for genome in genomes:

                genome_hit_count += 1
                if self.args.limit is not None and genome_hit_count > self.args.limit:
                    continue

                genome_hit = dict(
                    genome_id=genome['genome_info']['genome_id'],
                    reference_genome_id=genome['genome_info']['reference_genome_id'],
                    common_name=genome['genome_info']['common_name'],
                    scientific_name=genome['genome_info']['scientific_name'],
                    assembly_name=genome['genome_info']['assembly_name'],
                )

                for match_in_genome_name_type, match_info in genome['matches_info'].items():
                    for offset, length in match_info['offsets'].items():
                            matched_substring = dict(
                                length=length,
                                offset=offset,
                                match=match_in_genome_name_type,
                            )
                            genome_hit.setdefault('matched_substrings', []).append(matched_substring)

                group.append(genome_hit)

            if group:
                response.setdefault('genome_matches', []).append(group)

        # If there are no matches, just respond with an empty list
        if 'genome_matches' not in response:
            response.setdefault('genome_matches', [])

        response['total_hits'] = total_matches

        return response


api.add_resource(Search, '/')
