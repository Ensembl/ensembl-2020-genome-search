
# TODO: Change this. Dont use global variables
all_tokens = {}

tokenization = Tokenization()

tokens  = tokenization.create_tokens(species.common_name)

for token in tokens:
    all_tokens.setdefault(token, []).append(species.url_name)
#    print(all_tokens)


# print(all_tokens)


with open(data_files_path + '/tokens.json', 'w') as token_file:
    json.dump(all_tokens, token_file)