import os

class Config:
    DATA_FILE_PATH = os.getcwd() + '/data_files'
    GENOME_STORE_FILE_PATH = DATA_FILE_PATH + '/genome_store.json'
    INDEX_FILE_PATH = DATA_FILE_PATH + '/index.json'
    KEYS_TO_INDEX = ['common_name', 'scientific_name', 'subtype']
    V_VERSION = 96
    NV_VERSION = 43
    MINIMUM_TOKEN_LENGTH = 3
    STOP_CHARS_MAPPING = {'_': ' ', '-': '', '(': ' ', ')': ' ', '[': ' ', ']': ' '}
    DEBUG = True
    GENOME_ID_VALID_CHARS = 'A-Za-z0-9'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

def get_config():
    return Config.__dict__
