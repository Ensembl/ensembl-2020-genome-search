import json
from flask import jsonify

class EnsemblRegion:
	def __init__(self,gid=None, rcode=None, rid=None, rstart=None, rend=None):
		self.genome_id = gid
		self.region_code = rcode
		self.region_id = rid
		self.start = int(rstart) if rstart else None
		self.end = int(rend) if rend else None
		self.is_valid = False
		self.is_region_code_valid = False
		self.is_region_id_valid = False
		self.is_region_start_valid = False
		self.is_region_end_valid = False
		self.is_all_valid = False
		self.is_partial_valid = False
		self.is_parseable = False
		
	def set_is_all_valid(self):
		self.is_all_valid = self.is_region_code_valid and self.is_region_id_valid and self.is_region_start_valid and self.is_region_end_valid

	def set_is_partial_valid(self):
		self.is_partial_valid = self.is_region_code_valid or self.is_region_id_valid or self.is_region_start_valid or self.is_region_end_valid

	def get_genome_id_response(self):
		return dict(value=self.genome_id, is_valid=self.is_valid, error_message=None, error_code=None)

	def get_start_response(self):
		return dict(value=self.start, is_valid=self.is_region_start_valid, error_message=None, error_code=None)

	def get_end_response(self):
		return dict(value=self.end, is_valid=self.is_region_end_valid, error_message=None, error_code=None)

	def get_region_response(self):
		return  {
					"value" : self.region_id,
					"is_valid" : self.is_region_id_valid,
					"error_message" : None,
					"error_code" : None
					}
				
	def get_dict_response(self):
		dict_response = {
					"is_parseable" : self.is_parseable,
					"genome_id" : self.get_genome_id_response(),
					self.region_code : self.get_region_response(),
					"start" : self.get_start_response(),
					"end": self.get_end_response()
					}
		return dict_response

	def serialize(self):
		sero = dict(genome_id=self.genome_id)
		print (self.is_all_valid, self.is_partial_valid)
		if self.is_all_valid:
			sero = jsonify(self.get_dict_response())
		elif self.is_partial_valid:
			sero = jsonify(self.get_dict_response())
		else: 
			sero = jsonify(self.get_dict_response())
		return sero

