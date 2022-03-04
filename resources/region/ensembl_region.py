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

import json
from flask import jsonify

class EnsemblRegion:
	def __init__(self,gid=None, rcode=None, rname=None, rstart=None, rend=None):
		self.genome_id = gid
		self.region_code = rcode
		self.region_name = rname
		self.start = int(rstart) if isinstance(rstart, int) else None
		self.end = int(rend) if isinstance(rend, int) else None
		self.is_genome_id_valid = False
		self.is_region_code_valid = False
		self.is_region_name_valid = False
		self.is_region_start_valid = False
		self.is_region_end_valid = False
		self.is_region_valid = False
		self.is_all_valid = False
		self.is_partial_valid = False
		self.is_parseable = False
		self.is_valid = False
		self.start_error_message = None
		self.end_error_message = None
		self.region_code_error_message = None
		self.region_name_error_message = None
		self.region_error_message = None
		self.genome_id_error_message = None
		self.region_id  = None
		
	def set_is_all_valid(self):
		self.is_all_valid = self.is_region_valid and self.is_region_code_valid and self.is_region_name_valid and self.is_region_start_valid and self.is_region_end_valid

	def set_is_partial_valid(self):
		self.is_partial_valid = self.is_region_valid or self.is_region_code_valid or self.is_region_name_valid or self.is_region_start_valid or self.is_region_end_valid

	def get_genome_id_response(self):
		return dict(value=self.genome_id, \
					is_valid=self.is_genome_id_valid, \
					error_message=self.genome_id_error_message, \
					error_code=None)

	def get_start_response(self):
		return dict(value=self.start, \
					is_valid=self.is_region_start_valid, \
					error_message=self.start_error_message, \
					error_code=None)

	def get_end_response(self):
		return dict(value=self.end, \
					is_valid=self.is_region_end_valid, \
					error_message=self.end_error_message, \
					error_code=None)

	def get_region_response(self):
		return  {
					"region_code" : self.region_code,
					"region_name" : self.region_name,
					"is_valid" : self.is_region_valid,
					"error_message" : self.region_error_message,
					"error_code" : None
					}

	def generate_region_id(self):
		# 3704ceb1-948d-11ec-a39d-005056b38ce3:region:17:64155265-64255266
		# <genome_id>:region:<region_name<:<start>-<end>
		self.region_id = "{}:{}-{}".format(self.region_name,self.start,self.end)
		return self.region_id
		


	def get_dict_response(self):
		dict_response = {}
		# returns 400 if its not parseable
		# dict_response['is_parseable'] = self.is_parseable
		dict_response['genome_id'] = self.get_genome_id_response()
		dict_response['region_id'] = self.region_id
		if self.region_code:
			dict_response["region"] = self.get_region_response()
			dict_response['start']=self.get_start_response()
			dict_response['end']=self.get_end_response()			
		else:
			# invalid region_code # what to do ??
			dict_response["region"] = self.get_region_response()
			dict_response['start']=self.get_start_response()
			dict_response['end']=self.get_end_response()
		return dict_response

	def serialize(self):
		sero = jsonify(self.get_dict_response())
		return sero

