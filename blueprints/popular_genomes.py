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

from flask import Blueprint, jsonify, make_response, abort, url_for
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
import os, yaml

popular_genomes_bp = Blueprint('popular_genomes', __name__)
api = Api(popular_genomes_bp)


class PopularGenomes(Resource):
    def get(self, **kwargs):


        with open('configs/additional_configs.yaml') as f:
            data = yaml.safe_load(f)

        popular_genomes_response = {}

        for genome_id in data['POPULAR_GENOMES']:

            popular_genome = {}
            genome_data = data['POPULAR_GENOMES'][genome_id]

            genome_key = app.genome_store.check_if_genome_exists('genome_id', genome_id)

            if genome_key:
                popular_genome = app.genome_store.get_genome(genome_key)
            else:
                popular_genome['genome_id'] = genome_id
                popular_genome['genome_id_for_url'] = genome_id
                popular_genome['popular_order'] = genome_data['Order']
                popular_genome['is_available'] = False

            popular_genome['svg_file'] = genome_data['Icon']

            popular_genomes_response = self._prepare_response(popular_genomes_response, popular_genome)

        popular_genomes_response['popular_species'].sort(key=lambda genome: genome['popular_order'])

        return make_response(jsonify(popular_genomes_response), 200)


    def _prepare_response(self, popular_genomes_response, popular_genome):

        popular_genome_info = dict(
            genome_id=popular_genome['genome_id'],
            genome_id_for_url=popular_genome['genome_id_for_url'],
            popular_order=popular_genome.get('popular_order'),
            is_available=popular_genome.get('is_available'),
            image=url_for('temp_static_blueprint.static', 
                          filename=popular_genome.get('svg_file'),
                          _external=True,
                          _scheme=os.environ.get('DEPLOYMENT_SCHEME') if 'DEPLOYMENT_SCHEME' in os.environ else 'http'),
            reference_genome_id=popular_genome['reference_genome_id'] if 'reference_genome_id' in popular_genome else '',
            common_name=popular_genome['common_name'] if 'common_name' in popular_genome else '',
            scientific_name=popular_genome['scientific_name'] if 'scientific_name' in popular_genome else '',
            assembly_name=popular_genome['assembly_name'] if 'assembly_name' in popular_genome else '',
        )

        popular_genomes_response.setdefault('popular_species', []).append(popular_genome_info)

        return popular_genomes_response


api.add_resource(PopularGenomes, '/')
