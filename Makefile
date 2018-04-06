
INFILE=double_biclique_unambiguous.lp


## Usage and tests
compress:
	python -m powergrasp data/$(INFILE) -o out/out.bbl
	python -m bubbletools validate out/out.bbl

test: t
t:
	pytest powergrasp test -vv --doctest-module


## Packaging
upload:
	python setup.py sdist upload


.PHONY: test t compress upload


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
hanging-bio-notree-cc0:
	$(MAKE) compress INFILE=hanging-bio-notree-cc0.lp
horrible_data:
	$(MAKE) compress INFILE=horrible_data.lp
inclusions:
	$(MAKE) compress INFILE=inclusions.lp
consider-included-nodes:
	$(MAKE) compress INFILE=consider-included-nodes.lp
multiple-optimals:
	$(MAKE) compress INFILE=multiple-optimals.lp
n8_d0:
	$(MAKE) compress INFILE=n8_d0.7.lp
one_edge:
	$(MAKE) compress INFILE=one_edge.lp
order:
	$(MAKE) compress INFILE=order.lp
partition:
	$(MAKE) compress INFILE=partition.lp
perfectfit:
	$(MAKE) compress INFILE=perfectfit.lp
pnode-to-clique:
	$(MAKE) compress INFILE=pnode-to-clique.lp
prio_deg:
	$(MAKE) compress INFILE=prio_deg.lp
quoting:
	$(MAKE) compress INFILE=quoting.lp
star:
	$(MAKE) compress INFILE=star.lp
testblocks:
	$(MAKE) compress INFILE=testblocks.lp
test-gml:
	$(MAKE) compress INFILE=test.gml
test-graphml:
	$(MAKE) compress INFILE=test.graphml
unclique:
	$(MAKE) compress INFILE=unclique.lp
variable-name:
	$(MAKE) compress INFILE=variable-name.gml
