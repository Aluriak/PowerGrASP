
INFILE=double_biclique_unambiguous.lp
TEST_CFG_FILE=

SHOW_DURATIONS=--durations=22
FAILED_FIRST=--ff

## Usage and tests
compress:
	python -m powergrasp data/$(INFILE) out/out.bbl
	python -m bubbletools validate out/out.bbl

config:
	python -m powergrasp --config

test: t
t:
	- mv powergrasp.cfg powergrasp.cfg.bak
	# try different option sets
	$(MAKE) _test_cfg_file TEST_CFG_FILE=default  # with default values
	$(MAKE) _test_cfg_file TEST_CFG_FILE=oneshot
	$(MAKE) _test_cfg_file TEST_CFG_FILE=manyoptions
	$(MAKE) _test_cfg_file TEST_CFG_FILE=nostarsearch
	rm powergrasp.cfg
	- mv powergrasp.cfg.bak powergrasp.cfg
_pure_tests:
	pytest powergrasp test -x -vv --doctest-module $(SHOW_DURATIONS) $(FAILED_FIRST)
_test_cfg_file:
	cp test/powergrasp.$(TEST_CFG_FILE).cfg powergrasp.cfg
	$(MAKE) _pure_tests  # with many options tweaked (edges from ASP, integrity,…)


## Packaging
make_dist:
	python setup.py sdist
upload:
	twine upload --repository pypi dist/PowerGrASP-*.tar.gz
release: fullrelease
fullrelease:
	fullrelease
install_deps:
	python -c "import configparser; c = configparser.ConfigParser(); c.read('setup.cfg'); print(c['options']['install_requires'])" | xargs pip install -U


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
thesis:
	$(MAKE) compress INFILE=thesis.lp
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
