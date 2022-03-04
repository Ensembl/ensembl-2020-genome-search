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

import os
import requests, urllib.parse as urlparse
import json
from configs.config import get_config
from resources.rest_client import EnsemblREST, EnsemblGRCH37REST

if __name__ == "__main__":
    config = get_config()
    rest_client = EnsemblREST()
    grch37_rest_client = EnsemblGRCH37REST()
    with open(config['REGION_INFO_FILE'],'w') as kf:
        regions_info = {}
        if os.path.exists(config['GENOME_STORE_FILE']):
            with open(config['GENOME_STORE_FILE'], "r") as genome_store_file:
                genome_store_data = json.load(genome_store_file)
                for gid, genome in genome_store_data.items():
                    print ("Processing Species {} with assembly {} ".format(genome['production_name'], genome['assembly_name']))
                    species_karyotypes = {}
                    species_name = genome['production_name']
                    if genome['assembly_name'] in ['GRCh37.p13']:
                        assembly_info = grch37_rest_client.get_assembly_info(species_name)
                    else:
                        assembly_info = rest_client.get_assembly_info(species_name)
                    karyotypes = assembly_info['karyotype']
                    for karyotype in karyotypes:
                        region_info = rest_client.get_region_info(species_name,karyotype)
                        region_info['type'] = region_info['coordinate_system']
                        region_info['name'] = karyotype
                        region_info['is_chromosome'] = True if region_info['is_chromosome'] else False
                        region_info['is_circular'] = True if region_info['is_circular'] else False
                        del region_info['coordinate_system']
                        del region_info['assembly_exception_type']
                        del region_info['assembly_name']
                        if region_info['type'] not in species_karyotypes.keys():
                            species_karyotypes[region_info['type'].lower()] = {}
                        species_karyotypes[region_info['type'].lower()][karyotype.lower()] = region_info
                    regions_info[genome['genome_id']] = species_karyotypes
            json.dump(regions_info,kf)

    """
    genomes = {'homo_sapiens':'3704ceb1-948d-11ec-a39d-005056b38ce3', \
                'triticum_aestivum':'a73357ab-93e7-11ec-a39d-005056b38ce3', \
                'plasmodium_falciparum':'a73356e1-93e7-11ec-a39d-005056b38ce3', \
                'escherichia_coli':'escherichia_coli_str_k_12_substr_mg1655_GCA_000005845_2', \
                'saccharomyces_cerevisiae':'a733574a-93e7-11ec-a39d-005056b38ce3_2', \
                'caenorhabditis_elegans':'a733550b-93e7-11ec-a39d-005056b38ce3'}
    grch37_genomes = {'homo_sapiens':'3704ceb1-948d-11ec-a39d-005056b38ce3'}
    rest_client = EnsemblREST()
    grch37_rest_client = EnsemblGRCH37REST()
    with open('karyotype_data.json','w') as kf:
        regions_info = {}
        for species_name in genomes.keys():
            species_karyotypes = []
            assembly_info = rest_client.get_assembly_info(species_name)
            karyotypes = assembly_info['karyotype']
            for karyotype in karyotypes:
                region_info = rest_client.get_region_info(species_name,karyotype)
                region_info['type'] = region_info['coordinate_system']
                del region_info['coordinate_system']
                del region_info['assembly_exception_type']
                del region_info['assembly_name']
                region_info['name'] = karyotype
                species_karyotypes.append(region_info)
            regions_info[genomes[species_name]] = species_karyotypes

        for species_name in grch37_genomes:
            species_karyotypes = []
            assembly_info = grch37_rest_client.get_assembly_info(species_name)
            karyotypes = assembly_info['karyotype']
            for karyotype in karyotypes:
                region_info = grch37_rest_client.get_region_info(species_name,karyotype)
                region_info['type'] = region_info['coordinate_system']
                del region_info['coordinate_system']
                del region_info['assembly_exception_type']
                del region_info['assembly_name']
                region_info['name'] = karyotype
                species_karyotypes.append(region_info)
            regions_info[grch37_genomes[species_name]] = species_karyotypes  
        json.dump(regions_info,kf)
    """
