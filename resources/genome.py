class Genome(object):
    def __init__(self, **species_info):

        # Use dict get method so that we get None value instead of KeyError when a key is not found
        self.genome = species_info.get('organism', {}).get('name')
        self.common_name = species_info.get('organism', {}).get('display_name')
        self.scientific_name = species_info.get('organism', {}).get('scientific_name')
        self.url_name = species_info.get('organism', {}).get('url_name')
        self.assembly = species_info.get('assembly', {}).get('assembly_name')
        self.test = species_info.get('test', {}).get('test')
        self.__process_strains_info(**species_info)

    def __process_strains_info(self, **species_info):

        if species_info.get('organism', {}).get('strain') is None:
            self.is_strain = True
            self.parent_species = species_info.get('organism', {}).get('scientific_name')
        else:
            self.is_strain = False
            self.parent_species = None