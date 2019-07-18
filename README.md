# Genome search
Genome search backend microservice for ensembl 2020

This repo manages following endpoints:
1. /api/genome_search/
2. /api/alternative_assemblies/
3. /api/popular_genomes/
4. /api/genome/info/
5. /api/genome/track_categories/
6. /api/ensembl_object/
7. /api/ensembl_object/track_list/

## Data generation
Data generation has two steps:
1. Create Genome store file
2. Index Genome store file

Location of Genome store file and Index file are configured in configuration file.

### Genome store
Genome store file holds all the required data of the genomes we use on Ensembl website. It uses Ensembl Metadata Registry as its primary data source. We could populate genome store either by fetching data by division or by individual genome or load from file.
While fetching data, if genome store file already exists, it checks for genome ids in the existing genome store and does creation and updation accordingly.

Examples:

Fetch individual genomes:
```
python dump_species.py --fetch_by_genome Homo_sapiens Triticum_aestivum Caenorhabditis_elegans
```

Fetch by division:
```
python dump_species.py --fetch_by_division EnsemblVertebrates EnsemblMetazoa EnsemblPlants EnsemblFungi EnsemblProtists EnsemblBacteria
```

Load from file(useful when data is not present on metadata registry - example: GRCh37 data):
```
python dump_species.py --create_from_file /usr/src/genome-search/configs/grch37.json
```

If you created/updated only a few genomes in an existing genome store, you may want to know the genome store keys of those updated genomes. Use ```return_genome_store_ids``` in such cases. This could be useful when you want to index only newly created/updated genomes.

Example:
```
python dump_species.py --fetch_by_genome Homo_sapiens Triticum_aestivum Caenorhabditis_elegans --return_genome_store_ids
```

### Indexing
We could either index the whole genome store at a time or only a few genomes from genome store if needed. 

At the moment, only common name, scientific name and assembly name of a given genome are indexed. This can be changed in configuration yaml file.

Indexing is done by using edge n-gram tokens with a minimum token length of 3. 

Run indexer as follows.
To index whole genome store:
```
python index_species.py 
```
To index only a few genome store entries:
```
python index_species.py --index_genome_store_ids <ID_LIST>
```

## Testing
All the tests are located in tests directory and can be run using the following command:
```
python -m unittest discover -s tests
```
