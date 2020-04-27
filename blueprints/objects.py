from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
from resources.ensembl_rest import EnsemblRest
import yaml, requests, json, urllib.parse as urlparse, re


objects_bp = Blueprint('objects', __name__)
api = Api(objects_bp)


class ObjectInfo(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        parser.add_argument('type',  type=str, required=True, help="Missing type param in the request.", location='args')
        parser.add_argument('stable_id',  type=str, required=True, help="Missing stable_id param in the request.", location='args')
        self.args = parser.parse_args()

        if not self.args.genome_id:
            return abort(400, {'error': 'No value for genome_id'})
        if not self.args.type:
            return abort(400, {'error': 'No value for type'})
        if not self.args.stable_id:
            return abort(400, {'error': 'No value for stable_id'})

        genome_id = self.args.genome_id
        object_type = self.args.type
        object_value = self.args.stable_id
        
        genome_key = app.genome_store.check_if_genome_exists('genome_id', genome_id)

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID: {}'.format(genome_id)})

        if object_type == 'region':
            response = self.__prepare_region_response(genome_id, object_type, object_value)
            return make_response(jsonify(response), 200)
        else:

            # Get old e! unique identifier to query e! REST API
            genome_info = app.genome_store.get_genome(genome_key)
            production_name = genome_info.get('production_name')

            query_params = {'species': production_name, 'content-type': 'application/json'}

            # Configure to connect to right REST API
            if genome_info.get('assembly_name') == 'GRCh37':
                rest_url = app.config.get('BACKEND_GRCH37_REST_URL')
            else:
                rest_url = app.config.get('BACKEND_GENERIC_REST_URL')

            # Build the endpoint to get data from
            rest_url += '/lookup/id/' + object_value

            # Connect to REST API and fetch data
            rest_api = EnsemblRest()
            rest_response = rest_api.do_rest_request(url=rest_url, query_params=query_params)

            if rest_response.status_code != 200:
                return abort(400, {'error': 'Problem getting data'})
            else:
                response = json.loads(rest_response.text)

            # Prepare response. There may be different response structures for different object_types
            if object_type in ['gene', 'transcript']:
                response = self.__prepare_gene_response(genome_id, object_type, object_value, response)
                return make_response(jsonify(response), 200)
            elif object_type == 'transcript':
                return abort(400, {'error': 'Not supported yet'})
            elif object_type == 'variation':
                return abort(400, {'error': 'variation objects info not supported yet'})
            elif object_type == 'protein':
                return abort(400, {'error': 'protein objects info not supported yet'})
            else:
                return abort(400, {'error': '{} - object type not supported'.format(object_type)})

    def __prepare_region_response(self, genome_id, object_type, object_value):

        try:
            chromosome, coordinates = object_value.split(':')
            start, end = coordinates.split('-')
        except:
            return abort(400, {'error': 'Problem parsing region id'})

        response_data = dict(
            location=dict(
                chromosome=chromosome,
                start=start,
                end=end
            ),
            object_id=self.args.object_id,
            genome_id=genome_id,
            object_type=object_type,
            label=object_value
        )

        return response_data

    def __prepare_gene_response(self, genome_id, object_type, object_value, response):

        response_data = dict(
            bio_type=response.get('biotype').replace('_', ' ').capitalize() if response.get('biotype') is not None else None,
            # Return object_value if there is no display name in Ensembl REST response
            label=response.get('display_name', object_value),
            location=dict(
                chromosome=response.get('seq_region_name'),
                start=response.get('start'),
                end=response.get('end')
            ),
            strand='forward' if response.get('strand') == 1 else 'reverse',
            description=re.sub(r'\[.*?\]', '', response.get('description')).rstrip() if response.get('description') is not None else None,
            versioned_stable_id="{}.{}".format(object_value, response.get('version')) if response.get('version') is not None else None,
            genome_id=genome_id,
            type=object_type,
            stable_id=object_value
        )

        return response_data

    def __prepare_transcript_response(self):
        pass

    def __prepare_protein_response(self):
        pass

    def __prepare_variation_response(self):
        pass



class ObjectTrack(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        parser.add_argument('object_id', type=str, required=True, help="Missing object_id param in the request.",
                            location='args')
        self.args = parser.parse_args()
        if not self.args.genome_id:
            return abort(400, {'error': 'No value for genome_id'})

        genome_id = self.args.genome_id

        try:
            object_type, object_value = self.args.object_id.split(':')
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
            track_id='track:gene-feat',
            description=full_data.get('description')
        )

        for child_object_type, child_objects in full_data.get('child_objects').items():
            for child_object_id, child_object in child_objects.items():
                child_track_info.setdefault('child_tracks', []).append(
                    dict(
                        additional_info=child_object.get('additional_info'),
                        colour=child_object.get('colour'),
                        label=child_object_id,
                        ensembl_object_id='{}:{}'.format(child_object_type, child_object_id),
                        support_level=child_object.get('support_level'),
                        track_id='track:{}'.format(child_object.get('track_id')),
                        description=child_object.get('description')
                    )
                )

        response_data.update(child_track_info)

        return make_response(jsonify(response_data), 200)


api.add_resource(ObjectInfo, 'info/')
api.add_resource(ObjectTrack, 'track_list/')

