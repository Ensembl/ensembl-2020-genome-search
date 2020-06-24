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
