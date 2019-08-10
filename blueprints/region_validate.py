from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
from resources.region.ensembl_region import EnsemblRegion
from resources.region.ensembl_region_parser import  EnsemblRegionParser
import ipdb

region_validate_bp = Blueprint('region', __name__)
api = Api(region_validate_bp)

class RegionValidate(Resource):
    vro = EnsemblRegion()

    def get(self, **kwargs):

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        parser.add_argument('region',  type=str, required=True, help="Missing region param in the request.", location='args')

        self.args = parser.parse_args()
        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)
        iregion = self.args.region

        if genome_key is None:
            return abort(400, {'error': 'Invalid Genome ID'})

        ris = app.region_info_store

        validate_response = {}
        if self.args.genome_id in ris.keys():

            region_info_data = app.region_info_store[self.args.genome_id]
            self._parse_region(iregion)
            self.vro.is_valid = True
            self._validate_region()
            self.vro.set_is_all_valid()
            self.vro.set_is_partial_valid()
            validate_response = self.vro.serialize()
            return make_response(validate_response, 200)
        else:
            return abort(400, {'error': 'Invalid Genome ID'})
        return make_response(validate_response, 200)

    def _parse_region(self, iregion):
        erp = EnsemblRegionParser()
        #ro = EnsemblRegion()
        if erp.parse_subject(iregion):
            pr_valid = erp.parse_region()
            pl_valid = erp.parse_location()
            if pr_valid and pl_valid:
                erp.is_parseable = True
                self.vro = EnsemblRegion(self.args.genome_id, erp.region_code, erp.region_id, erp.start, erp.end)
                self.vro.is_parseable = True
            else:
                erp.is_parseable = False
                self.vro.is_parseable = False
        return self.vro

    def _validate_region(self):
        try :
            if self.vro.genome_id and self.vro.region_id:
                region = app.region_info_store[self.vro.genome_id][self.vro.region_id]
                self.vro.is_region_id_valid = True
                if region['is_circular']:
                    if  self.vro.start > self.vro.end:
                        self.vro.is_region_end_valid = False
                        self.vro.is_region_start_valid = False
                        return
                    # For cicular regions check if end is out of bound
                    if self.vro.end > region['length'] or self.vro.end < 1:
                        self.vro.is_region_end_valid = False
                    else:
                        self.vro.is_region_end_valid = True
                    # For cicular regions check if start is out of bound
                    if self.vro.start > region['length'] or self.vro.start < 1:
                        self.vro.is_region_start_valid = False
                    else:
                        self.vro.is_region_start_valid = True                
                else:
                    # Check if start is less than end
                    if  self.vro.start > self.vro.end:
                        self.vro.is_region_end_valid = False
                        self.vro.is_region_start_valid = False
                        return
                    # For linear region check if end is out of bound
                    if self.vro.end > region['length'] or self.vro.end < 1:
                        self.vro.is_region_end_valid = False
                    else:
                        self.vro.is_region_end_valid = True
                    print (self.vro.start, region['length'])
                    # For linear region check if end is out of bound
                    if self.vro.start > region['length'] or self.vro.start < 1:
                        self.vro.is_region_start_valid = False
                    else:
                        self.vro.is_region_start_valid = True
            else:
                print ("Cound not get region information")
        except KeyError as ke:
            pass
        except Exception as ex:
            pass
#    def _prepare_response(self, ero):#

#        alt_assemblies_info = dict(
#            assembly_name=alt_genome['assembly_name'],
#            genome_id=alt_genome['genome_id']
#        )#

#        alt_assemblies_response.setdefault('alternative_assemblies', []).append(alt_assemblies_info)#

#        return alt_assemblies_response


# Tests
# api/genome/region/validate?genome_id=escherichia_coli_str_k_12_substr_mg1655_GCA_000005845_2&region=chromosome%20Chromosome:123-26365
# Valid


api.add_resource(RegionValidate, '/validate')
