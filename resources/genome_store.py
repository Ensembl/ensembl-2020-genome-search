from resources.genome import Genome

class GenomeStore(object):
    def __init__(self, genome_store = {}):
        self.genome_store = genome_store

    def get_genome_store(self):
        return self.genome_store

    def get_next_genome(self):
        for genome_key, genome in self.genome_store.items():
            yield genome_key, genome


    def get_max_key(self):
        return int(max(self.genome_store.keys(), default=0,  key=(lambda k: int(k))))

    def get_genome(self, genome_key):
        return self.genome_store.get(genome_key)

    def check_if_genome_exists(self, genome_sub_key, genome_sub_value):
        for genome_key, genome in self.genome_store.items():
            if genome_sub_key in genome and genome[genome_sub_key] == genome_sub_value:
                return genome_key

    def add_to_genome_store(self, genome):

        existing_genome_key = self.check_if_genome_exists('genome_id', genome.genome_id)

        if existing_genome_key is not None:
            # TODO: Logic for updating existing genome

            existing_genome = Genome(self.get_genome(existing_genome_key))
            existing_genome.create_genome_from_genome_store()
            existing_genome.division.extend(genome.division)

            self.genome_store[existing_genome_key] = existing_genome.convert_to_dict()

        else:
            genome_key = self.get_max_key() + 1
            self.genome_store[genome_key] = genome.convert_to_dict()

