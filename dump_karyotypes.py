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
                    species_karyotypes = []
                    species_name = genome['production_name']
                    if genome['assembly_name'] in ['GRCh37.p13']:
                        assembly_info = grch37_rest_client.get_assembly_info(species_name)
                    else:
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
                    regions_info[genome['genome_id']] = species_karyotypes
            json.dump(regions_info,kf)

    """
    genomes = {'homo_sapiens':'homo_sapiens_GCA_000001405_27', \
                'triticum_aestivum':'triticum_aestivum_GCA_900519105_1', \
                'plasmodium_falciparum':'plasmodium_falciparum_GCA_000002765_2', \
                'escherichia_coli':'escherichia_coli_str_k_12_substr_mg1655_GCA_000005845_2', \
                'saccharomyces_cerevisiae':'saccharomyces_cerevisiae_GCA_000146045_2', \
                'caenorhabditis_elegans':'caenorhabditis_elegans_GCA_000002985_3'}
    grch37_genomes = {'homo_sapiens':'homo_sapiens_GCA_000001405_14'}
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
