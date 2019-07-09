# 0002. Object identifiers

Date: 2019-06-11

## Status

Agreed

## Context

To uniquely identify an object in Ensembl we need three pieces of information:

-   The **dataset** to which the object belongs, e.g. homo_sapiens_GCA_000001405_14 [^1]
-   The **object type**, e.g. gene, transcript, region  
-   The **object ID**, e.g. ENSG00000139618, AT3G52430, 13:32315474-32400266 [^2]  
  
Ensembl objects are used extensively in the web client and passing around three separate pieces of information for each one can be cumbersome, error prone, and adds additional work when serialisation is required (e.g. for use in URLs or hash keys).  

[^1]: For our purposes dataset can be considered synonymous to genome_id
[^2]: Region strings are not IDs but we can consider them that way in this case

## Decision

To allow more convenient manipulation of Ensembl objects we will use a string to uniquely identify each object. These “object IDs” will be generated and parsed by the back-end APIs, and should not be generated or parsed by the client (i.e. the client should not assume anything about the ID format). When the client needs information about an object it will request it through the relevant API calls.

Object ID format

`<dataset>:<object type>:<object id>`

Examples
```
homo_sapiens_GCA_000001405_14:gene:ENSG00000139618
arabidopsis_thaliana_GCA_000001735_1:gene:AT3G52430
arabidopsis_thaliana_GCA_000001735_1:transcript:AT3G52430
homo_sapiens_GCA_000001405_14:location:13:32315474-32400266
```
## Consequences

While it is convenient to have a human readable object ID format, a potential risk is that external users will make assumptions about how these IDs are composed. This may lead to attempted use of invalid IDs, or to external dependencies on a specific format.

At present, we feel the convenience of a human-readable format outweighs the potential risks.

However, as the web client does not parse the object IDs it should be possible to use alternative serialisation formats by changing the way IDs are generated and parsed in the back-end APIs.

An example of an alternative serialisation format is Base64 encoding, e.g.

Format

`Base64( <dataset>:<object type>:<object id> )`

Example
```
Base64( homo_sapiens_GCA_000001405_14:gene:ENSG00000139618 )
=>
aG9tb19zYXBpZW5zX0dDQV8wMDAwMDE0MDVfMTQ6Z2VuZTpFTlNHMDAwMDAxMzk2MTg=
```
In this case the object IDs cannot be easily decomposed by external users.
