from resources.region.region_parser import RegionParser
from resources.region.ensembl_region import EnsemblRegion
import re

class EnsemblRegionParser:
	def __init__(self):
		RegionParser.__init__(self, rcode=None, rname=None)
		self.subject_regex = re.compile(r'(.*):(.*)')
		self.region_regex = re.compile(r'(.*)\s+(.*)')
		self.location_regex = re.compile(r'(\d+)')
		self.location_pair_regex = re.compile(r'(\d+)-(\d+)')



	def parse_subject(self, istring):
		"""
		Purpose : Sets region_subject and location_subject from subject if matches.
		Returns : True if successfully matched region_subject, location_object else False
		For ex. 'Primary_assembly QNTS01000739.1: 292,231-374,157' extracts 
				 region_subject = Primary_assembly QNTS01000739.1
				 location_subject = 292,231-374,157
		"""
		try:
			token_matches = self.subject_regex.match(istring)
			match_groups = token_matches.groups()
			if match_groups:
				self.region_subject = match_groups[0].strip()
				self.location_subject = match_groups[1].strip().replace(',','')
				return True
			else:
				return False

		except Exception as ps_ex:
			pass

		return False

	def parse_region_name(self):
		"""
		Purpose: Given region_subject it Sets region_code, region_name
		Returns : True/False 

		"""
		try:
			if self.region_subject:
				region_tokens_match = self.region_regex.match(self.region_subject)
				if region_tokens_match:
					region_match_groups = region_tokens_match.groups()
					self.region_code = region_match_groups[0].strip().lower()
					self.region_name = region_match_groups[1].strip().lower()
					return True
				else:
					self.region_name = self.region_subject.strip().lower()
					return True
			else:
				return False
		except Exception as pr_ex:
			print (pr_ex)
			return False
		return False

	def parse_location(self):
		try:
			if self.location_subject:
				location_pair_match = self.location_pair_regex.match(self.location_subject)
				if location_pair_match:
					location_pair_match_groups = location_pair_match.groups()
					# print (location_match_groups)
					if (len(location_pair_match_groups)) == 2:
						try:
							self.start = int(location_pair_match_groups[0].strip())
							self.end = int(location_pair_match_groups[1].strip())
							return True
						except ValueError as ve:
							return False
					else:
						return False
			else:
				return False
		except Exception as prl_ex:
			return False

if __name__ == "__main__":
	pass