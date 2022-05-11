#
#    See the NOTICE file distributed with this work for additional information
#    regarding copyright ownership.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

FROM python:3.9.6

# maintainer of the image
LABEL maintainer="sboddu@ebi.ac.uk"
# Environment variable
ENV PYTHONUNBUFFERED TRUE

COPY . /usr/src/genome-search

WORKDIR /usr/src/genome-search

RUN pip3 install --no-cache-dir -r requirements.txt \
    && python dump_species.py --fetch_by_genome Homo_sapiens Triticum_aestivum Caenorhabditis_elegans Escherichia_coli_str_k_12_substr_mg1655 Saccharomyces_cerevisiae Plasmodium_falciparum \
    && echo 'y' | python dump_species.py --create_from_file /usr/src/genome-search/configs/grch37.json \
    && echo 'y' | python index_species.py

EXPOSE 8011

CMD ["gunicorn","--bind=0.0.0.0:8011","--workers=10","--preload","app:app"]

