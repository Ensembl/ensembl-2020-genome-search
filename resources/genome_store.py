class GenomeStore(object):
    def __init__(self, genome_store = {}):
        self.genome_store = genome_store

    def get_genome_store(self):
        return self.genome_store

    def add_to_store(self, key, value):
        self.genome_store[key] = value

    def get_max_key(self):
        return max(self.genome_store, default=0)

    def check_if_genome_exists(self, genome_sub_key, genome_sub_value):
        pass

    def get_key_of_genome(self, genome_sub_key, genome_sub_value):
        pass

    def udpate_a_genome(self, genome_sub_key, genome_sub_value):
        pass
