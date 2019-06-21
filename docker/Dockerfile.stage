FROM python:3.7.2

# maintainer of the image
LABEL maintainer="sboddu@ebi.ac.uk"
# Environment variable
ENV PYTHONUNBUFFERED TRUE

RUN git clone --depth 1 https://github.com/Ensembl/ensembl-2020-genome-search.git /usr/src/genome-search

WORKDIR /usr/src/genome-search

RUN pip3 install --no-cache-dir -r requirements.txt \
    && python dump_species.py --fetch_by_division EnsemblVertebrates EnsemblMetazoa EnsemblPlants EnsemblFungi EnsemblProtists EnsemblBacteria \
    && echo 'y' | python dump_species.py --create_from_file /usr/src/genome-search/configs/grch37.json \
    && echo 'y' | python index_species.py 

EXPOSE 8011

CMD ["gunicorn","--bind=0.0.0.0:8011","--workers=10","--preload","app:app"]

