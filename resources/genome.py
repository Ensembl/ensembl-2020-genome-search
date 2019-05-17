import re
from configs.config import get_config


class Genome(object):
    config = get_config()

    # Allow only alpha numeric in genome_id
    genome_id_regex = re.compile('[^{}]'.format(config['GENOME_ID_VALID_CHARS']))

    def __init__(self, genome_info):
        self.genome_info = genome_info


    def create_genome_from_metadata(self):

        # Use dict get method so that we get None value instead of KeyError when a key is not found
        self.common_name = self.genome_info.get('organism', {}).get('display_name')
        self.scientific_name = self.genome_info.get('organism', {}).get('scientific_name')
        self.production_name = self.genome_info.get('organism', {}).get('name')

        self.subtype = self.genome_info.get('assembly', {}).get('assembly_name')
        self.assembly_name = self.genome_info.get('assembly', {}).get('assembly_name')
        self.assembly_accession = self.genome_info.get('assembly', {}).get('assembly_accession')

        self.division = [self.genome_info.get('division', {}).get('name')]

        self.genome_id = self.__assign_genome_id()
        self.__process_strains_info()


    def create_genome_from_genome_store(self):

        # Use dict get method so that we get None value instead of KeyError when a key is not found
        self.common_name = self.genome_info.get('common_name')
        self.scientific_name = self.genome_info.get('scientific_name')
        self.production_name = self.genome_info.get('production_name')

        self.subtype = self.genome_info.get('assembly_name')
        self.assembly_name = self.genome_info.get('assembly_name')
        self.assembly_accession = self.genome_info.get('assembly_accession')

        self.division = self.genome_info.get('division')

        self.genome_id = self.__assign_genome_id()
        self.__process_strains_info()




    def create_genome_from_somethinf_else(self):
        pass



    def __process_strains_info(self):

        # TODO: How do I get reference species genome_id?

        if self.genome_info.get('organism', {}).get('strain') is None:
            self.is_strain = True
            self.reference_genome_id = self.genome_info.get('organism', {}).get('name')
        else:
            self.is_strain = False
            self.reference_genome_id = None


    def __assign_genome_id(self):

        if self.assembly_name is None or \
                self.production_name is None:
            raise Exception(
                'Problem with species {}. Either Assembly name or Production does\'t exist. \n'
                'Assembly name: {}, \n'
                'Production name: {}'.format(self.common_name, self.assembly_name, self.production_name))
        else:
            if 'EnsemblBacteria' in self.division:
                genome_id = '{}_{}'.format(
                    Genome.genome_id_regex.sub('', self.production_name),
                    Genome.genome_id_regex.sub('', self.assembly_accession)
                )
            else:
                genome_id = '{}_{}'.format(
                    Genome.genome_id_regex.sub('', self.production_name),
                    Genome.genome_id_regex.sub('', self.assembly_name)
                )
            return genome_id.lower()

    def sanitize(self):
        """Removes unnecessary genome object data before creating json file for the genome"""
        self.__dict__.pop('genome_info')


    def convert_to_dict(self):
        if 'genome_info' in self.__dict__:
            self.__dict__.pop('genome_info')
        return self.__dict__