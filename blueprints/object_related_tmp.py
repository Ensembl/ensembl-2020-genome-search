from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
import os, yaml, sys

object_related_tmp_bp = Blueprint('object_related_tmp_bp', __name__)
api = Api(object_related_tmp_bp)


class ObjectInfo(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('object_id',  type=str, required=True, help="Missing object_id param in the request.", location='args')
        self.args = parser.parse_args()

        try:
            genome_id, object_type, object_value = self.args.object_id.split(':')
            print(genome_id, object_type, object_value)
        except:
            return abort(400, {'error': 'Problem parsing object_id'})

        with open('configs/flask_endpoints_tmp_configs/example_objects.yaml') as f:
            data = yaml.load(f)

        if genome_id not in data.keys():
            return abort(400, {'error': 'No data available for genome: {}'.format(genome_id)})
        elif object_type.title() not in data.get(genome_id).keys():
            return abort(400, {'error': "No data available for objects of type '{}' in genome: {}".format(object_type, genome_id)})
        elif object_value not in data.get(genome_id).get(object_type.title()).keys():
            return abort(400, {
                'error': 'No information about {} {} in genome: {}'.format(object_type, object_value, genome_id)})

        full_data = data.get(genome_id).get(object_type.title()).get(object_value)

        response_data = dict(
            bio_type=full_data.get('bio_type'),
            label=full_data.get('label'),
            ensembl_object_id=self.args.object_id,
            genome_id=genome_id,
            location=dict(
                chromosome=full_data.get('location').get('chromosome'),
                start=full_data.get('location').get('start'),
                end=full_data.get('location').get('end')
            ),
            object_type=object_type,
            spliced_length=full_data.get('spliced_length'),
            stable_id=object_value,
            strand=full_data.get('strand')
        )

        return make_response(jsonify(response_data), 200)




class ObjectTrack(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('object_id', type=str, required=True, help="Missing object_id param in the request.",
                            location='args')
        self.args = parser.parse_args()

        try:
            genome_id, object_type, object_value = self.args.object_id.split(':')
            print(genome_id, object_type, object_value)
        except:
            return abort(400, {'error': 'Problem parsing object_id'})

        with open('configs/flask_endpoints_tmp_configs/example_objects.yaml') as f:
            data = yaml.load(f)

        if genome_id not in data.keys():
            return abort(400, {'error': 'No data available for genome: {}'.format(genome_id)})
        elif object_type.title() not in data.get(genome_id).keys():
            return abort(400, {
                'error': "No data available for objects of type '{}' in genome: {}".format(object_type, genome_id)})
        elif object_value not in data.get(genome_id).get(object_type.title()).keys():
            return abort(400, {
                'error': 'No information about {} {} in genome: {}'.format(object_type, object_value, genome_id)})

        full_data = data.get(genome_id).get(object_type.title()).get(object_value)
        child_track_info = {}

        response_data = dict(
            additional_info=full_data.get('bio_type'),
            label=full_data.get('label'),
            ensembl_object_id=self.args.object_id,
            track_id='gene-feat')

        for child_object_type, child_objects in full_data.get('child_objects').items():
            for child_object_id, child_object in child_objects.items():
                child_track_info.setdefault('child_tracks', []).append(
                    dict(
                        additional_info=child_object.get('additional_info'),
                        colour=child_object.get('colour'),
                        label=child_object_id,
                        ensembl_object_id='{}:{}:{}'.format(genome_id, child_object_type, child_object_id),
                        support_level=child_object.get('support_level'),
                        track_id=child_object.get('track_id')
                    )
                )

        response_data.update(child_track_info)

        return make_response(jsonify(response_data), 200)


api.add_resource(ObjectInfo, 'info/')
api.add_resource(ObjectTrack, 'track_list/')

