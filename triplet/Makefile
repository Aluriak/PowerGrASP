
METHOD=search-byenum.lp
# METHOD=search-byconcept.lp
INFILE_DIR=../data
INFILE=double_biclique_unambiguous.lp
OPTIONS=

## Usage and tests
compress:
	# clingo 0 --opt-mode=optN -t 4 $(INFILE_DIR)/$(INFILE) $(METHOD)
	python search.py $(INFILE_DIR)/$(INFILE) $(METHOD) $(OPTIONS)

thesis:
	- rm out/*.png out/*.bbl
	$(MAKE) real-puceron-mi-m-diff-no3019 OPTIONS=""
	$(MAKE) real-puceron-mi-m-diff-no3019 OPTIONS="-na 3 -nb 3"
	$(MAKE) real-puceron-mi-m-diff-no3019 OPTIONS="-nc 2"
	$(MAKE) real-puceron-mi-m-diff-no3019 OPTIONS="-nc 3"
	$(MAKE) real-matrixdb-core27 OPTIONS=""
	$(MAKE) real-matrixdb-core27 OPTIONS="-na 3 -nb 3"
	$(MAKE) real-matrixdb-core27 OPTIONS="-nc 2"
	$(MAKE) real-matrixdb-core27 OPTIONS="-nc 3"

clear-cache:
	rm cases_cache/*.dat

## All real test cases
real-puceron-mi-m-diff:
	$(MAKE) compress INFILE_DIR=~/data/puceron/data-playing/output INFILE=miRNA_mRNA_diff.lp
real-puceron-mi-m-diff-no3019:
	$(MAKE) compress INFILE_DIR=~/data/puceron/data-playing/output INFILE=miRNA_mRNA_diff-no3019.lp
real-puceron-mi-lnc:
	$(MAKE) compress INFILE_DIR=~/data/puceron/data-playing/output INFILE=miRNA_lncRNA.lp
real-puceron-lnc-m:
	$(MAKE) compress INFILE_DIR=~/data/puceron/data-playing/output INFILE=lncRNA_mRNA.lp
real-puceron-mi-m-lnc:
	$(MAKE) compress INFILE_DIR=~/data/puceron/data-playing/output INFILE=ternary_concepts_mi_m_lnc-edge.lp
real-matrixdb-core27:
	$(MAKE) compress INFILE_DIR=~/data/MatrixDb/compmatrixdb/matrixdb_CORE27_example INFILE=matrixdb_CORE27_example.lp
real-matrixdb-all:
	$(MAKE) compress INFILE_DIR=~/data/MatrixDb/compmatrixdb/matrixdb_Human_Human_171107_extended INFILE=matrixdb_Human_Human_171107_extended_0.0.lp


## All test cases
abnormal:
	$(MAKE) compress INFILE=abnormal.lp
bintree:
	$(MAKE) compress INFILE=bintree.lp
clique:
	$(MAKE) compress INFILE=clique.lp
cliques:
	$(MAKE) compress INFILE=cliques.lp
concomp:
	$(MAKE) compress INFILE=concomp.lp
concept-loop:
	$(MAKE) compress INFILE=concept-loop.lp
ddiam:
	$(MAKE) compress INFILE=ddiam.lp
diacli:
	$(MAKE) compress INFILE=diacli.lp
diamond:
	$(MAKE) compress INFILE=diamond.lp
disjoint-subpnodes:
	$(MAKE) compress INFILE=disjoint-subpnodes.lp
double_biclique_unambiguous:
	$(MAKE) compress INFILE=double_biclique_unambiguous.lp
double-p-groups:
	$(MAKE) compress INFILE=double-p-groups.lp
hanging-bio-notree-cc0:
	$(MAKE) compress INFILE=hanging-bio-notree-cc0.lp
horrible_data:
	$(MAKE) compress INFILE=horrible_data.lp
inclusions:
	$(MAKE) compress INFILE=inclusions.lp
consider-included-nodes:
	$(MAKE) compress INFILE=consider-included-nodes.lp
motif-overlapping:
	$(MAKE) compress INFILE=motif-overlapping.lp
multiple-optimals:
	$(MAKE) compress INFILE=multiple-optimals.lp
n8_d0:
	$(MAKE) compress INFILE=n8_d0.7.lp
one_edge:
	$(MAKE) compress INFILE=one_edge.lp
order:
	$(MAKE) compress INFILE=order.lp
overlapping-bicliques:
	$(MAKE) compress INFILE=overlapping-bicliques.lp
partition:
	$(MAKE) compress INFILE=partition.lp
perfectfit:
	$(MAKE) compress INFILE=perfectfit.lp
phosphatase:
	$(MAKE) compress INFILE=phosphatase.lp
pnode-to-clique:
	$(MAKE) compress INFILE=pnode-to-clique.lp
prio_deg:
	$(MAKE) compress INFILE=prio_deg.lp
quasibiclique:
	$(MAKE) compress INFILE=quasibiclique.lp
quoting:
	$(MAKE) compress INFILE=quoting.lp
single-node:
	$(MAKE) compress INFILE=single-node.lp
star:
	$(MAKE) compress INFILE=star.lp
structural-binding:
	$(MAKE) compress INFILE=structural-binding.lp
structural-binding-maincc:
	$(MAKE) compress INFILE=structural-binding-maincc.lp
structural-binding-nobridge:
	$(MAKE) compress INFILE=structural-binding-nobridge.lp
testblocks:
	$(MAKE) compress INFILE=testblocks.lp
test-gml:
	$(MAKE) compress INFILE=test.gml
test-graphml:
	$(MAKE) compress INFILE=test.graphml
todel:
	$(MAKE) compress INFILE=todel.lp
triplets:
	$(MAKE) compress INFILE=triplets.lp
typical:
	$(MAKE) compress INFILE=typical-use-case.lp
unclique:
	$(MAKE) compress INFILE=unclique.lp
variable-name:
	$(MAKE) compress INFILE=variable-name.gml
wiki-tree-decomposition:
	$(MAKE) compress INFILE=wiki-tree-decomposition.lp
zorro:
	$(MAKE) compress INFILE=zorro.lp
