from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
import os, yaml

object_related_tmp_bp = Blueprint('object_related_tmp_bp', __name__)
api = Api(object_related_tmp_bp)


class ObjectInfo(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('object_id',  type=str, required=True, help="Missing object_id param in the request.", location='args')
        self.args = parser.parse_args()


        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID'})

        with open('configs/flask_endpoints_tmp_configs/track_categories.yaml') as f:
            data = yaml.load(f)
            return make_response(jsonify(data), 200)

        return make_response(jsonify(popular_genomes_response), 200)




class ObjectTrack(Resource):
    def get(self, **kwargs):


        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('object_id',  type=str, required=True, help="Missing object_id param in the request.", location='args')
        self.args = parser.parse_args()


        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID'})

        with open('configs/flask_endpoints_tmp_configs/track_categories.yaml') as f:
            data = yaml.load(f)
            return make_response(jsonify(data), 200)

        return make_response(jsonify(popular_genomes_response), 200)


api.add_resource(ObjectInfo, 'info/')
api.add_resource(ObjectTrack, 'track_list/')

