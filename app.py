"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from flask import Flask, make_response, jsonify, Blueprint
from flask_cors import CORS
import os, json, sys
from resources.genome_store import GenomeStore
from resources.ensembl_indexer import Indexer
from configs.config import get_config


from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Uncomment following while running with developement server
# run python app.py
"""
trace.set_tracer_provider(
TracerProvider(
        resource=Resource.create({SERVICE_NAME: "gss-dev"})
    )
)

tracer = trace.get_tracer(__name__)

# create a JaegerExporter
jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    #collector_endpoint='http://localhost:16686/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter, max_export_batch_size=10)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)
"""

def create_app():
    application = Flask(__name__)
    CORS(application)
    application.config.update(get_config())

    # Do not redirect branch URLs without / to URL with the one with /
    application.url_map.strict_slashes = False

    application.indexes = Indexer(open_data_file(application.config['INDEX_FILE']))
    print("Loaded indexes")
    application.genome_store = GenomeStore(open_data_file(application.config['GENOME_STORE_FILE']))
    print("Loaded Genome store")

    application.region_info_store = open_data_file(application.config['REGION_INFO_FILE'])
    print("Loaded Region info Store")

    with application.app_context():
        from blueprints import genome_search

        application.register_blueprint(genome_search.search_bp, url_prefix='/api/genome_search')

        from blueprints import alternative_assemblies
        application.register_blueprint(alternative_assemblies.alt_assemblies_bp, url_prefix='/api/alternative_assemblies')

        from blueprints import popular_genomes
        application.register_blueprint(popular_genomes.popular_genomes_bp, url_prefix='/api/popular_genomes')

        from blueprints import genomes
        application.register_blueprint(genomes.genomes_bp, url_prefix='/api/genome/')

        from blueprints import objects
        application.register_blueprint(objects.objects_bp, url_prefix='/api/object/')

        from blueprints import region_info
        application.register_blueprint(region_info.region_info_bp, url_prefix='/api/genome/karyotype/')

        from blueprints import region_validate
        application.register_blueprint(region_validate.region_validate_bp, url_prefix='/api/genome/region')

        application.register_blueprint(Blueprint('temp_static_blueprint', __name__, static_folder='static', static_url_path='/static/genome_images'))

        # print(application.url_map.iter_rules)

    # TODO: errorhandlers listening to only 404 errors at the moment. Needs investigating.
    register_generic_error_handlers(application)

    return application



def register_generic_error_handlers(application):

    @application.errorhandler(404)
    def not_found(error):
        #print('4040404040404')
        return make_response(jsonify({'error': 'Not found'}), 404)

    @application.errorhandler(405)
    def not_found(error):
        return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

    @application.errorhandler(500)
    def internal_error(error):
        #print('500500500500')
        return make_response(jsonify({'message': 'Internal Server Errorsss'}), 500)


def open_data_file(file):
    try:
        with open(file, 'r') as fh:
            contents = json.load(fh)
    except FileNotFoundError as fnf_error:
        sys.exit("Could not find the file {}\nExiting".format(file))
    except IOError as ioe_error:
        sys.exit("Problem reading file {}\nExiting!".format(file))
    except Exception as e:
        print("Unexpected error occurred while handling data files.\nExiting!")
        raise
    else:
        return contents



print("Starting the server...")

#### use gunicorn app:app --workers 2 --preload

app = create_app()

FlaskInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()


if __name__ == "__main__":
   #print(app.error_handler_spec)
   app.run(host="0.0.0.0", port=8011)
