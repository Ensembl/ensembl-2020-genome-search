from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse

region_info_bp = Blueprint('region_info', __name__)
api = Api(region_info_bp)

class RegionInfo(Resource):
    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        self.args = parser.parse_args()
        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID'})

        ris = app.region_info_store

        region_info_response = []
        if self.args.genome_id in ris.keys():
        	region_info_response = app.region_info_store[self.args.genome_id]

        return make_response(jsonify(region_info_response), 200)

    def _prepare_response(self, alt_assemblies_response, alt_genome):

        alt_assemblies_info = dict(
            assembly_name=alt_genome['assembly_name'],
            genome_id=alt_genome['genome_id']
        )

        alt_assemblies_response.setdefault('alternative_assemblies', []).append(alt_assemblies_info)

        return alt_assemblies_response


api.add_resource(RegionInfo, '/')
