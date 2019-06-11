from flask import Blueprint, jsonify, make_response, abort, url_for
from flask import current_app as app
from flask_restful import Resource, Api, reqparse

popular_genomes = Blueprint('popular_genomes', __name__)
api = Api(popular_genomes)


class PopularGenomes(Resource):
    def get(self, **kwargs):

        genome_keys = app.genome_store.get_all_matched_genome_keys('is_popular', True)

        if not genome_keys:
            return make_response(jsonify([]), 200)

        popular_genomes_response = {}

        for genome_key in genome_keys:
            popular_genome = app.genome_store.get_genome(genome_key)
            popular_genomes_response = self._prepare_response(popular_genomes_response, popular_genome)


        return make_response(jsonify(popular_genomes_response), 200)



    def _prepare_response(self, popular_genomes_response, popular_genome):

        popular_genome_info = dict(
            genome_id=popular_genome['genome_id'],
            reference_genome_id=popular_genome['reference_genome_id'],
            common_name=popular_genome['common_name'],
            scientific_name=popular_genome['scientific_name'],
            assembly_name=popular_genome['assembly_name'],
            image=url_for('static', filename="{}.svg".format(popular_genome['genome_id']), _external=True),
            division_ids=popular_genome['division'],
            is_available=popular_genome.get('is_available')
        )

        popular_genomes_response.setdefault('popular_species', []).append(popular_genome_info)

        return popular_genomes_response


api.add_resource(PopularGenomes, '/')
