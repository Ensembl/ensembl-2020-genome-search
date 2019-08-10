import re

class RegionParser:

	def __init__(self, sname=None, rcode=None, rid=None):
		self.genome_id = sname
		self.region = None
		self.start = None
		self.end = None
		self.subject_regex = None
		self.region_regex = None
		self.location_regex = None
		self.region_subject = None
		self.location_subject = None
		self.region_code = rcode
		self.region_id = rid
		self.is_parseable = False


	def parse_subject(self, istring):
		pass

	def parse_region(self):
		pass

	def parse_location(self):
		pass
