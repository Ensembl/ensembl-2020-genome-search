from flask import Blueprint, jsonify, make_response, abort
from flask import current_app as app
from flask_restful import Resource, Api, reqparse
from resources.region.ensembl_region import EnsemblRegion
from resources.region.ensembl_region_parser import  EnsemblRegionParser

region_validate_bp = Blueprint('region', __name__)
api = Api(region_validate_bp)

class RegionValidate(Resource):

    def get(self, **kwargs):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('genome_id',  type=str, required=True, help="Missing genome_id param in the request.", location='args')
        parser.add_argument('region',  type=str, required=True, help="Missing region param in the request.", location='args')
        parser.add_argument('region_code',  type=str, required=False, help="region_code is required.", location='args')
        parser.add_argument('region_id',  type=str, required=False, help="region_id is required.", location='args')

        self.args = parser.parse_args()
        genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)
        iregion = self.args.region
        iregion_code = self.args.region_code
        iregion_id = self.args.region_id

        self.vro = EnsemblRegion()

        # Check if genome_id is provided as param and exist in genome_store
        if self.args.genome_id:
            self.vro.genome_id = self.args.genome_id
            if self.args.genome_id not in app.region_info_store:
                self.vro.genome_id_error_message = "Cound not find genome {}".format(self.args.genome_id)
                validate_response = self.vro.serialize()
                return make_response(validate_response, 200)
        else:
            self.vro.genome_id_error_message = "Missing genome_id param in the request."
            validate_response = self.vro.serialize()
            return make_response(validate_response, 200)

        if iregion_code:
            self.vro.region_code = iregion_code.lower()

        if iregion_id:
            self.vro.region_id = iregion_id.lower()

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
            self.vro = None
            return make_response(validate_response, 200)
        else:
            self.vro = None
            return abort(400, {'error': 'Invalid Genome ID'})
            validate_response = self.vro.serialize()
            self.vro = None
            return make_response(validate_response, 200)

    def _parse_region(self, iregion):
        erp = EnsemblRegionParser()
        #ro = EnsemblRegion()
        if erp.parse_subject(iregion): 
            pr_valid = erp.parse_region()
            pl_valid = erp.parse_location()
            if pr_valid and pl_valid:
                erp.is_parseable = True
                if self.vro.region_code:
                    self.vro = EnsemblRegion(self.args.genome_id, self.vro.region_code, erp.region_id, erp.start, erp.end)
                elif erp.region_code:
                    self.vro = EnsemblRegion(self.args.genome_id, erp.region_code, erp.region_id, erp.start, erp.end)
                else:
                    return abort(400, {'error': 'region_code is required'})

                if self.vro.region_id:
                    self.vro = EnsemblRegion(self.args.genome_id, self.vro.region_code, self.vro.region_id, erp.start, erp.end)
                elif erp.region_id:
                    self.vro = EnsemblRegion(self.args.genome_id, erp.region_code, erp.region_id, erp.start, erp.end)
                else:
                    return abort(400, {'error': 'region_id is required'})
                self.vro.is_parseable = True
            else:
                erp.is_parseable = False
                self.vro.is_parseable = False
             
    def _validate_region(self):
        try :
            if self.vro.genome_id and self.vro.region_id:
                species_regions = app.region_info_store[self.vro.genome_id][self.vro.region_code]
                region = species_regions[self.vro.region_id]
                self.vro.is_region_id_valid = True
                if region['is_circular']:
                    
                    # For cicular regions check if start is out of bound
                    if self.vro.start > region['length']:
                        self.vro.is_region_start_valid = False
                        self.vro.start_error_message = "Start:{} can not be greater than {} for region {}".format(self.vro.start,region['length'],self.vro.region_id)
                    elif self.vro.start < 1:
                        self.vro.is_region_start_valid = False
                        self.vro.start_error_message = "Start:{} can not be less than 1 for region {}".format(self.vro.start, self.vro.region_id)
                    else:
                        self.vro.is_region_start_valid = True

                       
                    # For cicular regions check if end is out of bound
                    if self.vro.end > region['length']:
                        self.vro.is_region_end_valid = False
                        self.vro.end_error_message = "End:{} can not be greater than {} for region {}".format(self.vro.end,region['length'], self.vro.region_id)
                    elif self.vro.end < 1:
                        self.vro.end_error_message = "End:{} can not be less than 1 for region {}".format(self.vro.end, self.vro.region_id)
                    else:
                        self.vro.is_region_end_valid = True
                
                else:
                    if self.vro.start > region['length']:
                        self.vro.is_region_start_valid = False
                        self.vro.start_error_message = "start:{} can not be greater than {} for region {}".format(self.vro.start,region['length'],self.vro.region_id)
                    elif self.vro.start < 1:
                        self.vro.is_region_start_valid = False
                        self.vro.start_error_message = "start:{} can not be less than 1 for region {}".format(self.vro.start, self.vro.region_id)
                    else:
                        self.vro.is_region_start_valid = True

                    # For linear region check if end is out of bound
                    if self.vro.end > region['length']:
                        self.vro.is_region_end_valid = False
                        self.vro.end_error_message = "end:{} can not be greater than {} for region {}".format(self.vro.end,region['length'], self.vro.region_id)
                    elif self.vro.end < 1:
                        self.vro.end_error_message = "end:{} can not be less than 1 for region {}".format(self.vro.end, self.vro.region_id)
                    else:
                        self.vro.is_region_end_valid = True

                    # Check if start is less than end
                    if  self.vro.is_region_start_valid and self.vro.is_region_start_valid and self.vro.start > self.vro.end:
                        self.vro.is_region_end_valid = False
                        self.vro.is_region_start_valid = False
                        self.vro.start_error_message = "start:{} can not be greater than end:{} for region {}".format(self.vro.start, self.vro.end, self.vro.region_id)
                        return
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

# /api/genome/region/validate?genome_id=homo_sapiens_GCA_000001405_27&region=chromosome%20%20%201:123-262&region_code=chromosome
# Valid

# /api/genome/region/validate?genome_id=homo_sapiens_GCA_000001405_27&region=%20%20%201:123-262
# Valid

api.add_resource(RegionValidate, '/validate')
