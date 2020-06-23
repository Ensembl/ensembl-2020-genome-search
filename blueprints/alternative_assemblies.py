#
#    See the NOTICE file distributed with this work for additional information
#    regarding copyright ownership.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse

alt_assemblies_bp = Blueprint('alternative_assemblies', __name__)
api = Api(alt_assemblies_bp)


class AltAssemblies(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        self.args = parser.parse_args()

        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID'})

        genome = app.genome_store.get_genome(genome_key)

        if genome['alternative_assemblies'] is None:
            return make_response(jsonify([]), 200)

        alt_assemblies_response = {}
        for alt_assembly_genome_id in genome['alternative_assemblies']:
            alt_genome_key = app.genome_store.check_if_genome_exists('genome_id', alt_assembly_genome_id)

            # Check in case there is a corrupt alternative genome id loaded into genome store from configs
            if alt_genome_key is not None:
                alt_genome = app.genome_store.get_genome(alt_genome_key)
                alt_assemblies_response = self._prepare_response(alt_assemblies_response, alt_genome)


        return make_response(jsonify(alt_assemblies_response), 200)



    def _prepare_response(self, alt_assemblies_response, alt_genome):

        alt_assemblies_info = dict(
            assembly_name=alt_genome['assembly_name'],
            genome_id=alt_genome['genome_id']
        )

        alt_assemblies_response.setdefault('alternative_assemblies', []).append(alt_assemblies_info)

        return alt_assemblies_response


api.add_resource(AltAssemblies, '/')
