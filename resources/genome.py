class Genome(object):
    def __init__(self, **species_info):

        self.species_info = species_info

        # Use dict get method so that we get None value instead of KeyError when a key is not found
        self.common_name = species_info.get('organism', {}).get('display_name')
        self.scientific_name = species_info.get('organism', {}).get('scientific_name')
        self.url_name = species_info.get('organism', {}).get('url_name')
        self.subtype = species_info.get('assembly', {}).get('assembly_name')
        self.division = [species_info.get('division', {}).get('name')]

        self.genome_id = self.__assign_genome_id()
        self.__process_strains_info()

    def __process_strains_info(self):

        # TODO: How do I get reference species genome_id?

        if self.species_info.get('organism', {}).get('strain') is None:
            self.is_strain = True
            self.reference_genome_id = self.species_info.get('organism', {}).get('name')
        else:
            self.is_strain = False
            self.reference_genome_id = None

    def __assign_genome_id(self):

        # TODO: For all genomes except that belong to bacteria, genome_id is sanitised (production_name(undescore)assembly_name). For Bacterial genomes, if assembly_name exists, it would be sanitised (production_name(undescore)assembly_name) else it would be sanitised (production_name(undescore)GCA_accession number)

        if 'assembly_name' not in self.species_info['assembly']:
            raise Exception('No assembly name for species {}'.format(self.species_info['organism']['display_name']))
        else:
            return self.species_info['assembly']['assembly_name']

    def sanitize(self):
        """Removes unnecessary genome object data before creating json file for the genome"""
        self.__dict__.pop('species_info')
