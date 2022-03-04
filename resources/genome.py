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
from configs.config import get_config


class Genome(object):
    config = get_config()

    # Allow only alpha numeric in genome_id
    genome_id_regex = re.compile('[^{}+]'.format(config['GENOME_ID_VALID_CHARS']))
 
    genome_uuids = {} 
    genome_uuids['escherichia_coli_str_k_12_substr_mg1655_gca_000005845_GCA_000005845_2'] = 'a73351f7-93e7-11ec-a39d-005056b38ce3'
    genome_uuids['caenorhabditis_elegans_GCA_000002985_3'] = 'a733550b-93e7-11ec-a39d-005056b38ce3'
    genome_uuids['homo_sapiens_GCA_000001405_28'] = 'a7335667-93e7-11ec-a39d-005056b38ce3'
    genome_uuids['plasmodium_falciparum_GCA_000002765_2'] = 'a73356e1-93e7-11ec-a39d-005056b38ce3'
    genome_uuids['saccharomyces_cerevisiae_GCA_000146045_2'] = 'a733574a-93e7-11ec-a39d-005056b38ce3'
    genome_uuids['triticum_aestivum_GCA_900519105_1'] = 'a73357ab-93e7-11ec-a39d-005056b38ce3'
    genome_uuids['homo_sapiens_GCA_000001405_14'] = '3704ceb1-948d-11ec-a39d-005056b38ce3'

    def __init__(self, genome_info):
        self.genome_info = genome_info

    def create_genome_from_mr_format(self):

        # Use dict get method so that we get None value instead of KeyError when a key is not found
        mr_display_name = self.genome_info.get('organism', {}).get('display_name')
        mr_scientific_name = self.genome_info.get('organism', {}).get('scientific_name')

        if mr_display_name == mr_scientific_name:
            self.common_name = None
        else:
            self.common_name = mr_display_name

        self.scientific_name = self.genome_info.get('organism', {}).get('scientific_name')
        self.production_name = self.genome_info.get('organism', {}).get('name')

        self.assembly_name = self.genome_info.get('assembly', {}).get('assembly_name')
        self.assembly_accession = self.genome_info.get('assembly', {}).get('assembly_accession')

        self.division = [self.genome_info.get('division', {}).get('name')]

        self.genome_id = self.__assign_genome_id()
        self.alternative_assemblies = self.__find_alternative_assemblies()

        self.is_popular = self.__check_if_is_popular()

        if self.is_popular:
            self.popular_order = self.__get_popular_order()

        self.is_available = self.__check_if_is_available()

        if self.is_available:
            self.example_objects = self.__get_example_objects()

        self.__process_strains_info()

    def create_genome_from_gs_format(self):

        self.__dict__.update(self.genome_info)
        self.sanitize()

    def create_genome_from_something_else(self):
        pass

    def __process_strains_info(self):

        # TODO: How do I get reference species genome_id?

        if self.genome_info.get('organism', {}).get('strain') is not None:
            self.is_strain = True
            self.reference_genome_id = self.genome_info.get('organism', {}).get('name')
        else:
            self.is_strain = False
            self.reference_genome_id = None

    def __assign_genome_id(self):

        # Tmp hack until GCA value is loaded into Metadata registry
        if self.production_name == 'plasmodium_falciparum':
            genome_id_key = 'plasmodium_falciparum_GCA_000002765_2'
            return self.genome_uuids[genome_id_key]

        if self.assembly_accession is None and \
                self.assembly_name is None:
            raise Exception(
                'Problem with species {}. Either Assembly name or Assembly accession does\'t exist. \n'
                'Assembly name: {}, \n'
                'Assembly accession: {}'.format(self.common_name, self.assembly_name, self.assembly_accession))
        else:
                genome_id_key = '{}_{}'.format(
                    Genome.genome_id_regex.sub('_', self.production_name),
                    Genome.genome_id_regex.sub('_', self.assembly_accession if self.assembly_accession else self.assembly_name))

                return self.genome_uuids[genome_id_key]

    def __find_alternative_assemblies(self):

        if 'ASSOCIATED_ASSEMBLIES' in self.config:
            for associated_assemblies in self.config['ASSOCIATED_ASSEMBLIES'].values():
                if self.genome_id in associated_assemblies:
                    associated_assemblies.remove(self.genome_id)
                    return associated_assemblies
        return None

    def __check_if_is_popular(self):

        if 'POPULAR_GENOMES' in self.config and self.genome_id in self.config['POPULAR_GENOMES']:
            return True
        else:
            return False

    def __get_popular_order(self):

        return self.config['POPULAR_GENOMES'][self.genome_id]['Order']

    def __check_if_is_available(self):

        if 'AVAILABLE_GENOMES' in self.config and self.genome_id in self.config['AVAILABLE_GENOMES']:
            return True
        else:
            return False

    def __get_example_objects(self):

        return self.config['AVAILABLE_GENOMES'].get(self.genome_id)

    def sanitize(self):
        """Removes unnecessary genome object data before creating json file for the genome"""
        self.__dict__.pop('genome_info')

    def convert_to_dict(self):
        if 'genome_info' in self.__dict__:
            self.__dict__.pop('genome_info')
        return self.__dict__
