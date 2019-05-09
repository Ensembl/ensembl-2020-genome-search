class GenomeStore(object):
    def __init__(self, genome_store = {}):
        self.genome_store = genome_store

    def get_genome_store(self):
        return self.genome_store

    def get_next_genome(self):
        for genome_key, genome in self.genome_store.items():
            yield genome_key, genome

    def add_to_store(self, key, value):
        self.genome_store[key] = value

    def get_max_key(self):
        return int(max(self.genome_store.keys(), default=0,  key=(lambda k: int(k))))

    def get_genome(self, genome_key):
        return self.genome_store.get(genome_key)


    def check_if_genome_exists(self, genome_sub_key, genome_sub_value):
        pass

    def get_key_of_genome(self, genome_sub_key, genome_sub_value):
        pass

    def udpate_a_genome(self, genome_sub_key, genome_sub_value):
        pass
