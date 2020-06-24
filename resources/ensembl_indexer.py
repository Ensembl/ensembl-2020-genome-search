from configs.config import get_config


class Indexer(object):
    def __init__(self, indexes={}):
        self.indexes = indexes

    def add_to_index(self, token, genome_key):
        self.indexes.setdefault(token.lower(), []).append(genome_key)
        self.indexes.update({token.lower(): list(set(self.indexes[token.lower()]))})

    def search(self, user_input):
        return self.indexes.get(user_input.lower())

    def get_indexes(self):
        return self.indexes


class Tokenize(object):
    def __init__(self, **kwargs):

        config = get_config()

        self.stop_char_mapping = config['STOP_CHARS_MAPPING']
        self.min_token_length = config['MINIMUM_TOKEN_LENGTH']

    def create_tokens(self, string):

        # Replace stop characters using stop character mapping
        translation_table = string.maketrans(self.stop_char_mapping)
        string = string.translate(translation_table)

        # Create a list of tokens by splitting the string
        tokens = string.split()

        # Remove leading 0s
        tokens = list(map(lambda s: s.lstrip('0'), tokens))

        # Create Edge ngram tokens
        edge_ngram_tokens = []
        for token in tokens:
            for i in range(self.min_token_length, len(token) + 1):
                edge_ngram_tokens.append(token[:i])
        return edge_ngram_tokens
