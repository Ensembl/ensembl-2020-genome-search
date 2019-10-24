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
                processed_example_objects.append("{}:{}:{}".format(genome['genome_id'], object_type.lower(), object_value))

            genome.update({'example_objects': processed_example_objects})

        return genome


class GenomeTracks(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        self.args = parser.parse_args()

        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID'})
        genome_id = self.args.genome_id
        track_cat_response_data = {}
        track_cat_response_data['track_categories'] = []
        with open('configs/flask_endpoints_tmp_configs/track_categories.yaml') as f:
            data = yaml.load(f)
            track_cats = data['genome_track_categories']
            if genome_id in track_cats.keys():
                track_cat_response_data['track_categories'] = track_cats[genome_id]

        return make_response(jsonify(track_cat_response_data), 200)




api.add_resource(GenomeInfo, 'info/')
api.add_resource(GenomeTracks, 'track_categories/')
