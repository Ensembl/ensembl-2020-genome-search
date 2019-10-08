import re

class RegionParser:
	"""
	Purpose : Given subject string, parse subject string based in predefined 
			  regular expression.
			  If subject is parseable it sets
			  	parseable to true and also 
			  	sets region_name, start, end attribute
			  	optionally 
			  	sets region_code attribute
			  else
				ets parseable to False
	"""

	def __init__(self, rcode=None, rname=None):
		self.region = None
		self.start = None
		self.end = None
		self.subject_regex = None
		self.region_regex = None
		self.location_regex = None
		self.region_subject = None
		self.location_subject = None
		self.region_code = rcode
		self.region_name = rname
		self.is_parseable = False


	def parse_subject(self, istring):
		pass

	def parse_region_name(self):
		pass

	def parse_location(self):
		pass
