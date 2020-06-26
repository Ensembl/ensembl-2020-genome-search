# 0003. Genome identifiers

Date: 2020-02-20

## Status

Agreed. Supersedes [0001-genome-identifiers](0001-genome-identifiers.md)

## Context

Genome id has to serve a twofold purpose:

1. It must uniquely identify a combination of an assembly and a dataset (annotation set), so that users have an opportunity at any point to return to the same biological feature they viewed in the past and see it exactly the same as when they last viewed it, despite its annotation having potentially changed with a new data release.
2. At the same time, genome id is a part of the url, and as such is presented to the search engine. We want users who are arriving to Ensembl from a search engine to see the biological entity with the most current annotation set.

Additionally, we want to offer users an opportunity to view a dataset even before it has been properly released (partial/upcoming release), in a similar way as some software producers offer nightly releases of software for developers or testers.

## Decision

There will be two sets of genome ids:

1. A uuid assigned to every combination of assembly and dataset. This solves the problem of selecting any of the data releases for a given assembly that the user may be interested in.
2. An id that refers to the "best" (i.e. latest) data for a given assembly.

Conceptually, this is similar to git, which has hashes unique for every commit, and branches, which preserve their names between commits, but whose head always points at the latest commit. Similarly, genome uuids will change every time a new dataset is released for an assembly, but the "best" id will remain the same and will correspond to the uuid of the latest dataset for a given assembly.

"Best" ids can be short and human-readable.

For example:
- https://ensembl.org/browser/grch38/...
- https://ensembl.org/browser/grch37/...
- https://ensembl.org/browser/zfin10/...
- https://ensembl.org/browser/wheat/...

The table below demonstrates how uuids for an assembly change from release to release, but the "best" id remains the same and always points at the uuid corresponding to the latest dataset.

|          | e!103                                |  e!102                               |  e!101                               |
|----------|--------------------------------------|--------------------------------------|--------------------------------------|
| grch38 → | 7c4437b2-49c0-11ea-b77f-2e728ce88125 | 7c443bea-49c0-11ea-b77f-2e728ce88125 | 7c443d52-49c0-11ea-b77f-2e728ce88125 |


The idea of an upcoming release does not have to influence genome id, but rather can be reflected in the subdomain (codename "scary" — e.g. `https://scary.ensembl.org/browser/grch38/...`).

Pages for genome ids different from the "best" should contain a metatag identifying the page with the "best" genome id as "canonical" (`<link rel="canonical" href="https://ensembl.org/grch38/..." />`, see [Google’s recommendations for webmasters](https://support.google.com/webmasters/answer/139066)).
