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

from resources.genome import Genome


class GenomeStore(object):
    slug_genome_id_mapping = {
        "grch38"   : "homo_sapiens_GCA_000001405_28",
        "grch37"   : "homo_sapiens_GCA_000001405_14",
        "iwgsc"    : "triticum_aestivum_GCA_900519105_1",
        "r64-1-1"  : "saccharomyces_cerevisiae_GCA_000146045_2",
        "asm276v2" : "plasmodium_falciparum_GCA_000002765_2",
        "asm584v2" : "escherichia_coli_str_k_12_substr_mg1655_gca_000005845_GCA_000005845_2",
        "wbcel235" : "caenorhabditis_elegans_GCA_000002985_3"
        }

    def __init__(self, genome_store={}):
        self.genome_store = genome_store
        self.processed_genomes_list = set()

    def get_genomeid_from_slug(self, url_slug):
        if url_slug in self.slug_genome_id_mapping:
            return self.slug_genome_id_mapping[url_slug]
        return url_slug

    def get_genome_store(self):
        return self.genome_store

    def get_next_genome(self):
        for genome_key, genome in self.genome_store.items():
            yield genome_key, genome

    def get_max_key(self):
        return int(max(self.genome_store.keys(), default=0, key=(lambda k: int(k))))

    def get_genome(self, genome_key):
        # Make sure you return copy of the genome as any changes to
        # original genome would effect genome_store calls in subsequent
        # requests as we are using in memory genome store.
        return self.genome_store.get(genome_key).copy()

    # Todo: Merge check_if_genome_exists and get_all_matched_genome_keys based on calling context?

    def check_if_genome_exists(self, genome_sub_key, genome_sub_value):
        for genome_key, genome in self.genome_store.items():
            genome_sub_value = self.get_genomeid_from_slug(genome_sub_value)
            if genome_sub_key in genome and genome[genome_sub_key] == genome_sub_value:
                return genome_key


    def get_all_matched_genome_keys(self, genome_sub_key, genome_sub_value):
        matched = []
        for genome_key, genome in self.genome_store.items():
            if genome_sub_key in genome and genome[genome_sub_key] == genome_sub_value:
                matched.append(genome_key)
        return matched

    #    def update_genome_store(self, genome_key, genome_value):
    #        self.genome_store[genome_key] = genome_value

    def add_to_genome_store(self, genome):

        existing_genome_key = self.check_if_genome_exists('genome_id', genome.genome_id)

        if existing_genome_key is not None:
            # TODO: Logic for updating existing genome. At the moment, we are updating only division.

            existing_genome = Genome(self.get_genome(existing_genome_key))
            existing_genome.create_genome_from_gs_format()
            self.genome_store[existing_genome_key] = existing_genome.convert_to_dict()

            self.processed_genomes_list.add(existing_genome_key)

        else:
            genome_key = self.get_max_key() + 1
            self.genome_store[genome_key] = genome.convert_to_dict()
            self.processed_genomes_list.add(genome_key)
