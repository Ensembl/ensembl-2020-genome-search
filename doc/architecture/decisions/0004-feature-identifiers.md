# 0004. Genome identifiers

Date: 2020-03-20

## Status

Agreed. Supersedes [0002-object-identifiers](0002-object-identifiers.md)

## Context

According to the [0002-object-identifiers](0002-object-identifiers.md) proposal, a feature id (called object id in 0002) has the following format:

`<genome id>:<feature type>:<feature stable id>`

## Decision

1) Genome id should not be part of feature id. Genome id will be submitted to APIs in a separate field; which makes it redundant to repeat it in the feature id.
2) Feature type, however, should remain part of feature id, because Ensembl store features that share the same id, but belong to different types (e.g. genes or transcripts)

Therefore, the proposed format for feature identifiers is:

```
<feature type>:<feature stable id>
```

Examples:

```
gene:ENSG00000139618
transcript:AT3G52430
```

_Note:_ genome browser will include "regions" (spans of chromosome with a start and an end coordinate) in the list of features, which have meaning only in the context of genome browser, but are not considered features in other Ensembl applications. The proposed identifier format for regions is:

```
region:<region name>:<start coordinate>-<end coordinate>
```

example:
```
region:13:32315474-32400266
```
