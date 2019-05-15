import yaml, os, inspect

def get_config():
    self_dir = os.path.dirname(inspect.stack()[0][1])
    config_fn = os.path.join(self_dir, 'core_config.yaml')
    with open(config_fn) as config_f:
        config = yaml.load(config_f)

# TODO: Loop through all the key: value pairs and resolve the paths instead of doing it manually as follows

    config.update({'GENOME_STORE_FILE': config['DATA_FILE_PATH']+'/'+config['GENOME_STORE_FILE']})
    config.update({'INDEX_FILE': config['DATA_FILE_PATH']+'/'+config['INDEX_FILE']})

    return config

