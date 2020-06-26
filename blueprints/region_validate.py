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

        self.args = parser.parse_args()
        # genome_key = app.genome_store.check_if_genome_exists('genome_id', self.args.genome_id)
        iregion = self.args.region
        iregion_code = self.args.region_code
        
        self.vro = EnsemblRegion()

        # Check if genome_id is provided as param and exist in genome_store
        if self.args.genome_id:
            self.vro.genome_id = self.args.genome_id
            self.vro.is_genome_id_valid = True
            if self.args.genome_id not in app.region_info_store:
                self.vro.is_genome_id_valid = False
                self.vro.genome_id_error_message = "Cound not find region info for genome {}".format(self.args.genome_id)
                validate_response = self.vro.serialize()
                return make_response(validate_response, 200)
        else:
            self.vro.is_genome_id_valid = False
            self.vro.genome_id_error_message = "No value for genome_id"
            validate_response = self.vro.serialize()
            return make_response(validate_response, 200)

        if iregion_code:
            self.vro.region_code = iregion_code.lower()
        ris = app.region_info_store
        if iregion:
            validate_response = {}
            if self.vro.genome_id in ris.keys():
                self.vro.is_genome_id_valid = True
                region_info_data = app.region_info_store[self.vro.genome_id]
                if self._parse_region(iregion):
                    self.vro.is_genome_id_valid = True
                    self.vro.is_valid = True
                    self._validate_region()
                    self.vro.set_is_all_valid()
                    self.vro.set_is_partial_valid()
                    if self.vro.is_all_valid:
                        self.vro.generate_region_id()
                    validate_response = self.vro.serialize()
                    self.vro = None
                    return make_response(validate_response, 200)
                else:
                    return make_response(jsonify({'message': {'parse' : 'Could not parse region {}'.format(iregion) }}), 400)

            else:
                self.vro.genome_id_error_message = "Could not find genome_id"
                validate_response = self.vro.serialize()
                self.vro = None
                return make_response(validate_response, 200)
        else:
            self.vro.region_error_message = "No value for region"
            validate_response = self.vro.serialize()
            return make_response(validate_response, 200)

    def _parse_region(self, iregion):
        erp = EnsemblRegionParser()
        #ro = EnsemblRegion()
        if erp.parse_subject(iregion):
            pr_valid = erp.parse_region_name()
            pl_valid = erp.parse_location()
            if pr_valid and pl_valid:
                erp.is_parseable = True
                self.vro.is_parseable = True
                # if self.vro.region_code:
                #     self.vro = EnsemblRegion(self.args.genome_id, self.vro.region_code, erp.region_name, erp.start, erp.end)
                if erp.region_code:
                    self.vro.region_code = erp.region_code
                    # self.vro = EnsemblRegion(self.args.genome_id, erp.region_code, erp.region_name, erp.start, erp.end)
                # else:
                #     return abort(400, {'error': 'region_code is required'})

                if self.vro.region_name:
                    self.vro = EnsemblRegion(self.args.genome_id, self.vro.region_code, self.vro.region_name, erp.start, erp.end)
                elif erp.region_name:
                    self.vro = EnsemblRegion(self.args.genome_id, erp.region_code, erp.region_name, erp.start, erp.end)
                else:
                    return abort(400, {'message': 'region_name is required'})
                self.vro.is_parseable = True
                self.vro.start = erp.start
                self.vro.end = erp.end
                return True
            else:
                erp.is_parseable = False
                self.vro.is_parseable = False
        return False
             
    def _validate_start(self,region):
        try:
            self.vro.start = int(self.vro.start)
            if region['is_circular']:
                # For cicular regions check if start is out of bound
                if self.vro.start > region['length']:
                    self.vro.start_error_message = "Start should be between {} and {}".format(1,region['length'])
                    return False
                elif self.vro.start < 1:
                    self.vro.start_error_message = "Start should be between {} and {}".format(1,region['length'])
                    return False
                else:
                    self.vro.is_region_start_valid = True
                    return True
            else:
                if self.vro.start >= region['length']:
                    self.vro.start_error_message = "Start should be between {} and {}".format(1,region['length'])
                    return False
                elif self.vro.start < 1:
                    self.vro.start_error_message = "Start should be between {} and {}".format(1,region['length'])
                    return False
                else:
                    self.vro.is_region_start_valid = True
                    return True
        except ValueError as ve:
            self.vro.start_error_message = "Start should be number"
            return False
        except Exception as ex:
            self.vro.start_error_message = "Unknown Error"
            return False

    def _validate_end(self,region):
        try:
            self.vro.end = int(self.vro.end)
            if region['is_circular']:
                # For cicular regions check if end is out of bound
                if self.vro.end > region['length']:
                    self.vro.end_error_message = "End should be between {} and {}".format(1,region['length'])
                    return False
                elif self.vro.end < 1:
                    self.vro.end_error_message = "End should be between {} and {}".format(1,region['length'])
                    return False
                else:
                    self.vro.is_region_end_valid = True
                    return True
            else:
                if self.vro.end > region['length']:
                    self.vro.end_error_message = "End should be between {} and {}".format(1,region['length'])
                    return False
                elif self.vro.end < 1:
                    self.vro.end_error_message = "End should be between {} and {}".format(1,region['length'])
                    return False
                else:
                    self.vro.is_region_end_valid = True
                    return True
        except ValueError as ve:
            self.vro.end_error_message = "End should be number"
            return False
        except Exception as ex:
            self.vro.end_error_message = "Unknown Error"
            return False


    def _validate_location(self, region):
        # Check if start is less than end
        if  self.vro.is_region_start_valid and self.vro.is_region_end_valid:
            if region['is_circular']:
                return True
            else:                
                if self.vro.start > self.vro.end:
                    self.vro.is_region_start_valid = False
                    self.vro.start_error_message = "Start can not be greater than end".format(self.vro.start, self.vro.end)
                    return False
                else:
                    return True
        else:
            return False

    def _validate_region_size(self, region):
        # Check if the requested region has minimum size (bp)
        MINIMUM_REGION_SIZE = 50
        region_size_in_bp = self.vro.end - self.vro.start
        if region_size_in_bp < MINIMUM_REGION_SIZE:
            self.vro.region_error_message = "Region needs atleast {} basepair for visualisation.".format(MINIMUM_REGION_SIZE)
            return False
        return True


    def _validate_region(self):
        try :
            if self.vro.genome_id and self.vro.region_name:
                region_codes = app.region_info_store[self.vro.genome_id].keys()
                if self.vro.region_code:
                    if self.vro.region_code in region_codes:
                        self.vro.is_region_code_valid = True
                        species_regions = app.region_info_store[self.vro.genome_id][self.vro.region_code]
                        if self.vro.region_name:
                            if self.vro.region_name in species_regions.keys():
                                self.vro.is_region_name_valid = True
                                # self.vro.is_region_valid = True
                                region = species_regions[self.vro.region_name]
                                self.vro.is_region_start_valid = self._validate_start(region)
                                self.vro.is_region_end_valid = self._validate_end(region)
                                if self._validate_location(region):
                                    self.vro.is_region_valid = self._validate_region_size(region)
                                    self.vro.is_valid = self.vro.is_region_valid
                                else:
                                    self.vro.is_valid = False
                        else:
                            self.vro.region_error_message = "Region name is needed"
                    
                else:
                    for iregion_code in region_codes:
                        species_regions = app.region_info_store[self.vro.genome_id][iregion_code]
                        if self.vro.region_name in species_regions.keys():
                            region = species_regions[self.vro.region_name]
                            self.vro.is_region_code_valid = True
                            self.vro.is_region_name_valid = True
                            self.vro.is_region_valid = True
                            self.vro.region_code = region['type']
                            self.vro.is_region_start_valid = self._validate_start(region)
                            self.vro.is_region_end_valid = self._validate_end(region)
                            if self._validate_location(region):
                                self.vro.is_region_valid = self._validate_region_size(region)
                                self.vro.is_valid = self.vro.is_region_valid
                            else:
                                self.vro.is_valid = False
                            break
                        else:
                            self.vro.is_region_code_valid = False
                            self.vro.is_region_name_valid = False
                    if not self.vro.is_region_name_valid:
                        self.vro.region_error_message = "Could not find region {}".format(self.vro.region_name)

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
# Valid
# /api/genome/region/validate?genome_id=homo_sapiens_GCA_000001405_27&region=chromosome%201:123-26365343

# Valid
# /api/genome/region/validate?genome_id=homo_sapiens_GCA_000001405_27&region=1:123-26365343

# Valid
# /api/genome/region/validate?genome_id=homo_sapiens_GCA_000001405_27&region=chromosome%201:123-26365343


api.add_resource(RegionValidate, '/validate')
