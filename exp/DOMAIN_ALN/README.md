# Domain-based alignment

Models for protein evolution rely on accurate assignment of homologous sites in multiple sequence alignment.
However, sequence alignment of highly divergent gene families is often unreliable, leading to non-homologous sites being aligned together.
This affects the reconstruction of gene trees and can result in erroneous inference of copy number gain and loss events.

Hidden markov model (HMM) alignment has proven robust even in the case of divergent gene families, but relies on the availability of markov models.
In this experiment, I performed HMM alignment on protein domains that were inferred by matching the protein sequences of the mosquito genomes against
the PFAM database. 
Subsequently, protein sequences were decomposed into their predicted domains, and re-aligned. 
For each gene family, the alignment of its protein domains were concactenated into a single multiple sequence alignment. 

## Scan against PFAM

I downloaded the latest [PFAM](https://www.ebi.ac.uk/interpro/download/pfam/) database and scanned for domain hits accross all 4185 genes of Dataset 4.
The table showing all best hits for each domain against all 4185 genes is available [here](families_OG_4/proteins.domains.besthit.tsv).

![Histogram of domain hits per gene](families_OG_4/proteins.domains.besthit.hist.png?raw=true "Histogram of domain hits per gene")

520 out of 4185 genes in Dataset 4 have no significant hits to PFAM domains. 
![Genes with no significant PFAM hits](families_OG_4/proteins.domains.besthit.nohit.png?raw=true "Genes with no significant PFAM hits")

This affects 418 out of 1533 families, leaving 324 families with no domain hit in any of its members.
Most of these families have only a single member:

```
size #families
1    296
2     11
3      9
4      7
5      1
```
The following families with no hits have representatives in 3 or all species of Dataset 4:

```
family          #species
OG6150742       4
OG6126353       4
OG6126582       4
OG6186994       4
OG6151102       4
OG6124339       4
OG6124330       3
OG6315469       3
OG6162719       3
OG6r17102472    3
OG6142123       3
OG6132683       3
OG6132472       3
```

## Protein domain decomposition of genes

I filtered overlapping domain hits by lowest overall e-value and produced a [data set with no overlapping domain hits](https://github.com/cchauve/AGO-pipeline/blob/DOMAIN_ALN/exp/DOMAIN_ALN/families_OG_4/proteins.domains.besthit.nooverlap.tsv)

![Histogram of non-overlapping domain hits per gene](families_OG_4/proteins.domains.besthit.nooverlap.hist.png?raw=true "Histogram of domain hits per gene")

## Alignment & concatenation

I re-aligned each predicted protein domain with its corresponding HMM and concatenated alginment of all protein domains into a [family-wide alignment](https://github.com/cchauve/AGO-pipeline/blob/DOMAIN_ALN/exp/DOMAIN_ALN/families_OG_4/families_alignments.tar.gz)
