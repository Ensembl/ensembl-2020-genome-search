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
        self.char_translate = {'_': ' ', '-': '', '(': ' ', ')': ' ', '[': ' ', ']': ' '}
        self.min_token_length = 3

    def create_tokens(self, string):
        #       print(string)
        translation_table = string.maketrans(self.char_translate)
        translated_string = string.translate(translation_table)
        translated_string_splitted = translated_string.split(' ')
        leading_0s_removed = list(map(lambda s: s.lstrip('0'), translated_string_splitted))
        #       print(leading_0s_removed)
        edge_ngram_tokens = []
        for token in leading_0s_removed:
            for i in range(self.min_token_length, len(token) + 1):
                #           print(token[:i])
                edge_ngram_tokens.append(token[:i])
        return edge_ngram_tokens
