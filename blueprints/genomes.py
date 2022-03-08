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

from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
import yaml

genomes_bp = Blueprint('genomes', __name__)
api = Api(genomes_bp)


class GenomeInfo(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args', action='append')
        self.args = parser.parse_args()

        genome = {}

        for genome_id in self.args.genome_id:

            genome_key = app.genome_store.check_if_genome_exists('genome_id', genome_id)

            if genome_key is None:
                return abort(400, {'error': 'Invalid Genome ID: {}'.format(genome_id)})

            raw_genome = app.genome_store.get_genome(genome_key)

            processed_genome = self.__prepare_response(raw_genome)

            genome.setdefault('genome_info', []).append(processed_genome)

        return make_response(jsonify(genome), 200)

    def __prepare_response(self, genome):

        if 'example_objects' in genome:
            processed_example_objects = []
            for object_type, object_value in genome['example_objects'].items():
                ex_object = {}
                ex_object["type"] = object_type.lower()
                ex_object["id"] = object_value
                processed_example_objects.append(ex_object)

            genome.update({'example_objects': processed_example_objects})

        return genome

api.add_resource(GenomeInfo, 'info/')

