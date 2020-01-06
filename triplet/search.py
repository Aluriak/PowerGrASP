"""Search for triplets, generating graphics

TODO:
- nombre de concepts formels dans les graphiques

"""
import os
import sys
import pickle
import clyngor
import argparse
import itertools
import functools
from time import time
from collections import defaultdict
from pprint import pprint

import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
sns.set(style="whitegrid")
matplotlib.rcParams.update({
    # Use LaTeX to write all text
    "text.usetex": True,
    'font.sans-serif': 'Computer Modern Sans serif',
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

# sns.axes_style()

# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str,
                        help='file.lp containing the graph data')
    parser.add_argument('searchfile', type=str,
                        help='file.lp containing the motif search')
    parser.add_argument('--no-plot', '-np', action='store_true', default=False,
                        help='Plot the data as image files')
    parser.add_argument('--min-a', '-na', type=int, default=None,
                        help='minimal number of node in A')
    parser.add_argument('--min-b', '-nb', type=int, default=None,
                        help='minimal number of node in B')
    parser.add_argument('--min-c', '-nc', type=int, default=None,
                        help='minimal number of node in C')
    parser.add_argument('--max-a', '-ma', type=int, default=None,
                        help='maximal number of node in A')
    parser.add_argument('--max-b', '-mb', type=int, default=None,
                        help='maximal number of node in B')
    parser.add_argument('--max-c', '-mc', type=int, default=None,
                        help='maximal number of node in C')
    return parser.parse_args()

def is_canonical(a, b, c):
    if len(a) == 1 or len(b) == 1:
        return False
    if a and min(a) != min(a | b):
        return False
    return True


def compute_concepts() -> dict:
    """Compute formal concepts, yield them grouped by cover"""
    models = clyngor.solve((INFILE, 'compute-concepts.lp'), stats=False).by_predicate
    concepts = defaultdict(list)  # cover -> [concepts]
    nb_concepts = 0
    for model in models:
        nb_concepts += 1
        extent = frozenset(args[0] for args in model.get('ext', ()) if len(args) == 1)
        intent = frozenset(args[0] for args in model.get('int', ()) if len(args) == 1)
        a, b, c = extent - intent, intent - extent, extent & intent
        if MIN_A and len(a) < MIN_A or MAX_A and len(a) > MAX_A: continue
        if MIN_B and len(b) < MIN_B or MAX_B and len(b) > MAX_B: continue
        if MIN_C and len(c) < MIN_C or MAX_C and len(c) > MAX_C: continue
        cover = cover_from(a, b, c)
        concepts[cover].append((extent, intent))
    return nb_concepts, dict(concepts)

def cover_from(a:set, b:set, c:set) -> int:
    return int(len(a) * len(b) + len(a) * len(c) + len(b) * len(c) + (len(c)*(len(c)-1))/2)
assert cover_from({1, 2}, {3, 4}, {5, 6}) == 13
assert cover_from({1}, {3, 4}, {2, 5, 6}) == cover_from({}, {3, 4}, {1, 2, 5, 6})

def filter_non_maximal_triplets(triplets:[(set, set, set)]) -> [(set, set, set)]:
    """Yield given extended concepts (encoded as dict) that are contained by no other.
    Also remove doublons and non maximal triplets."""
    def extract_only_arg(it:frozenset) -> iter:
        yield from (obj for obj, in it)
    def as_ext_int(concept:tuple) -> (set, set):
        a, b, c = concept
        extent = frozenset(a | c)
        intent = frozenset(b | c)
        return extent, intent
    @functools.lru_cache()
    def edges_of(concept:(set, set), frozenset=frozenset, product=itertools.product) -> set:
        "Return set of all edges covered given concept"
        ext, int = concept
        return frozenset(frozenset((a, b)) for a in ext for b in int)
    concepts = tuple(triplets)
    all_concepts, concepts = concepts, tuple(set(concepts))
    print('#all: {}    #unique: {}'.format(len(all_concepts), len(concepts)))
    concepts_as_ext_int = tuple(map(as_ext_int, concepts))

    # remove non maximal triplets and doublons
    for idx, (concept, ext_int) in enumerate(zip(concepts, concepts_as_ext_int)):
        for candidate_idx, (candidate, candidate_ext_int) in enumerate(zip(concepts, concepts_as_ext_int)):  # we search candidate that contains the concept
            is_next = candidate_idx > idx  # the candidate is later in the order
            # print(f'COMPARING CONCEPTS {idx} and {candidate_idx} ({is_next}, {edges_of(candidate_ext_int) >= edges_of(ext_int)}, {edges_of(candidate_ext_int) > edges_of(ext_int)})')
            # keep only the bigger
            if edges_of(candidate_ext_int) > edges_of(ext_int):
                # print('\tdiscarded:', pretty_concept(ext_int))
                print('SUP:', edges_of(candidate_ext_int))
                print('EXTINT:', edges_of(ext_int))
                break
            # in case of equality, discard all but the last
            elif is_next and edges_of(candidate_ext_int) == edges_of(ext_int):
                # a future extended concept is equivalent. We can forgot the current one.
                print('\tdiscarded by equality:', pretty_concept(ext_int), '  ==  ', pretty_concept(candidate_ext_int))
                break
            # NB: the following would not work, since you would keep a concept
            #  if a previous one was bigger.
            # if is_next and edges_of(candidate_ext_int) >= edges_of(ext_int):
        else:  # no break, so no candidate was containing the concept
            yield concept

def get_triplets(edge_max=True):
    "Enumerate all triplet (concepts)"
    models = clyngor.solve((SEARCH, INFILE), options='-t 4 --opt-mode=optN', constants=constants).by_predicate
    print('COMMAND:', models.command)
    triplets = []
    best = 0
    def get_set_elems(model, name):
        return frozenset(args[0] for args in model.get(name, ()) if len(args) == 1)
    nb_admissible_triplet = 0
    for idx, model in enumerate(models, start=1):
        a, b, c = get_set_elems(model, 'a'), get_set_elems(model, 'b'), get_set_elems(model, 'c')
        triplets.append((a, b, c))
        cover = cover_from(a, b, c)
        best = best if best > cover else cover
        print(f'\r{idx}   {cover}/{best}      ', end='', flush=True)
        nb_admissible_triplet += 1
    if not triplets: return
    print()
    print(f'#admissible={nb_admissible_triplet}')
    if edge_max:
        start = time()
        nb_triplet_concept = 0
        for idx, (a, b, c) in enumerate(filter_non_maximal_triplets(triplets)):
            print('\r{}  t={}s      '.format(idx, round(time()-start,2)), end='', flush=True)
            yield a, b, c
            nb_triplet_concept += 1
        print()
        print(f'#triplet-concept={nb_triplet_concept}  ({round(nb_triplet_concept/nb_admissible_triplet*100, 2)}% of admissibles are maximal)')
    else:
        yield from triplets



args = parse_args()
INFILE = args.infile
SEARCH = args.searchfile
INFILE_NAME = os.path.splitext(os.path.basename(INFILE))[0]

MIN_A, MAX_A = args.min_a, args.max_a
MIN_B, MAX_B = args.min_b, args.max_b
MIN_C, MAX_C = args.min_c, args.max_c
constants = {}
if MIN_A is not None: constants['min_a'] = MIN_A
else: MIN_A = 0
if MIN_B is not None: constants['min_b'] = MIN_B
else: MIN_B = 0
if MIN_C is not None: constants['min_c'] = MIN_C
else: MIN_C = 0
if MAX_A is not None: constants['max_a'] = MAX_A
else: MAX_A = ''
if MAX_B is not None: constants['max_b'] = MAX_B
else: MAX_B = ''
if MAX_C is not None: constants['max_c'] = MAX_C
else: MAX_C = ''

INFILE_TO_PRETTY = {
    'miRNA_mRNA_diff': r'\textit{aphid RNA}',
    'miRNA_mRNA_diff-no3019': r'\textit{reduced RNA}',
    'matrixdb_CORE27': r'\textit{core MatrixDB}',
}
INFSYMB = '\\infty'
OUTSUFFIX = f'__a_{MIN_A}-{MAX_A}_b_{MIN_B}-{MAX_B}_c_{MIN_C}-{MAX_C}'
PRETTY_OUTSUFFIX = '\\quad'.join(e for e in (
    (f"$a \\in [{0 if MIN_A is None else MIN_A};{INFSYMB if MAX_A in {None, ''} else MAX_A}]$" if MIN_A != 0 or MAX_A != '' else ''),
    (f"$b \\in [{0 if MIN_B is None else MIN_B};{INFSYMB if MAX_B in {None, ''} else MAX_B}]$" if MIN_B != 0 or MAX_B != '' else ''),
    (f"$c \\in [{0 if MIN_C is None else MIN_C};{INFSYMB if MAX_C in {None, ''} else MAX_C}]$" if MIN_C != 0 or MAX_C != '' else '')
) if e)
CASE_NAME = f'{INFILE_NAME}{OUTSUFFIX}'
PRETTY_CASE_NAME = f"{INFILE_TO_PRETTY.get(INFILE_NAME, INFILE_NAME)}\n({PRETTY_OUTSUFFIX or 'no constraints'})".replace('_', ' ')
CASE_CONCEPT_PATHNAME = f'cases_cache/{CASE_NAME}.concepts.dat'
CASE_PATHNAME = f'cases_cache/{CASE_NAME}.dat'
CASE_PATHNAME_BBL = f'out/{CASE_NAME}.bbl'

BBL_REMAINING_NODES = True  # keep all nodes of the graph
BBL_REMAINING_EDGES = True  # keep all edges of the graph (between kept nodes only)

if os.path.exists(CASE_PATHNAME):  # already computed: get the cached data
    with open(CASE_PATHNAME, 'rb') as fd:
        triplets = pickle.load(fd)
    print(f'Data ({len(triplets)} entries)loaded from {CASE_PATHNAME}')
    search_stats = f'loaded from {CASE_PATHNAME}'
else:  # not already computed
    start = time()
    triplets = defaultdict(list)  # score: triplets
    best = 0
    all_triplets = get_triplets(edge_max=True)
    for idx, (a, b, c) in enumerate(all_triplets, start=1):
        if MIN_A and len(a) < MIN_A or MAX_A and len(a) > MAX_A: continue
        if MIN_B and len(b) < MIN_B or MAX_B and len(b) > MAX_B: continue
        if MIN_C and len(c) < MIN_C or MAX_C and len(c) > MAX_C: continue
        cover = cover_from(a, b, c)
        assert is_canonical(a, b, c)
        triplets[cover].append((a, b, c))
        best = best if best > cover else cover
        print(f'\r{idx}   {cover}/{best}      ', end='', flush=True)
    print()
    if triplets:
        assert best == max(triplets)
        search_stats = f'BEST score: {best}    ({len(triplets[best])} triplets)     (in {round(time() - start, 2)}s)'
        print(search_stats)
        for a, b, c in triplets[best]:
            pass
            # print()
            # print('   ', a)
            # print('   ', b)
            # print('   ', c)
    else:
        search_stats = f"No triplet generated for {CASE_NAME}"
        print(search_stats)
        print()
    print(f'Saving in {CASE_PATHNAME}…')
    with open(CASE_PATHNAME, 'wb') as fd:
        pickle.dump(triplets, fd)
print(f'Found {sum(map(len, triplets.values()))} triplets.')

if os.path.exists(CASE_CONCEPT_PATHNAME):  # already computed: get the cached data
    with open(CASE_CONCEPT_PATHNAME, 'rb') as fd:
        concepts = pickle.load(fd)
    print(f'Concepts data ({len(concepts)} entries) loaded from {CASE_CONCEPT_PATHNAME}')

else:
    print(f'Computing concepts…')
    start = time()
    nb_concepts, concepts = compute_concepts()
    print(f'Found {nb_concepts} concepts (max cover is {max(concepts) if concepts else "None"}) in {round(time() - start, 2)}s')
    print(f'Saving in {CASE_CONCEPT_PATHNAME}…')
    with open(CASE_CONCEPT_PATHNAME, 'wb') as fd:
        pickle.dump(concepts, fd)
print(f'Found {sum(map(len, concepts.values()))} concepts.')


def write_bubble(triplets, search_stats, compress_despite_overlaps:bool=True):
    triplets_in_cover_order = itertools.chain.from_iterable((  # from bigger to smaller
        triplets.get(idx, ())
        for idx in range(int(max(triplets)), int(min(triplets))-1, -1)
    )) if triplets else ()
    nodes = set()  # all nodes of the graph
    edges = set()  # all edges of the graph
    models = clyngor.solve(INFILE).by_predicate
    for model in models:
        for elems in map(frozenset, model.get('edge', ())):
            if len(elems) == 2:
                nodes |= elems
                edges.add(elems)
    treated_nodes = set()  # nodes belonging to a triplet
    with open(CASE_PATHNAME_BBL, 'w') as fd:
        fd.write('# bubble generated by ~/packages/powergrasp/triplet/search.py\n')
        fd.write('# ' + search_stats + '\n')
        write = lambda line: fd.write(line.replace('"', '') + '\n')
        if BBL_REMAINING_NODES:
            for node in nodes:
                write(f"NODE\t{node}")
        for idx, (a, b, c) in enumerate(triplets_in_cover_order, start=1):
            abc = a | b | c
            if abc & treated_nodes:
                if compress_despite_overlaps and (not a or a - treated_nodes) and (not b or b - treated_nodes) and (not c or c - treated_nodes):
                    # it's ok, there is enough nodes remaining
                    a -= treated_nodes
                    b -= treated_nodes
                    c -= treated_nodes
                    abc = a | b | c
                else:
                    # print(f'SKIPPED: {a} {b} {c} because of {abc & treated_nodes}')
                    continue  # already used
            # print('TRIPLET:', a, b, c)
            treated_nodes |= abc
            edges -= set(frozenset((x,y)) for x in a for y in b)
            edges -= set(frozenset((x,y)) for x in a for y in c)
            edges -= set(frozenset((x,y)) for x in b for y in c)
            edges -= set(frozenset((x,y)) for x in c for y in c)
            if len(a) > 2:
                a_node = f'A_{idx}'
                write(f'SET\t{a_node}\t1.0')
                for node in a:  write(f'IN\t{node}\t{a_node}')
            elif a:
                a_node = next(iter(a))
            if len(b) > 2:
                b_node = f'B_{idx}'
                write(f'SET\t{b_node}\t1.0')
                for node in b:  write(f'IN\t{node}\t{b_node}')
            elif b:
                b_node = next(iter(b))
            if len(c) > 2:
                c_node = f'C_{idx}'
                write(f'SET\t{c_node}\t1.0')
                for node in c:  write(f'IN\t{node}\t{c_node}')
            elif c:
                c_node = next(iter(c))
            if a and b: write(f'EDGE\t{a_node}\t{b_node}\t1.0')
            if a and c: write(f'EDGE\t{a_node}\t{c_node}\t1.0')
            if b and c: write(f'EDGE\t{b_node}\t{c_node}\t1.0')
            if len(c) > 2: write(f'EDGE\t{c_node}\t{c_node}\t1.0')
        if BBL_REMAINING_EDGES:
            for x, y in edges:
                if BBL_REMAINING_NODES or x in treated_nodes and y in treated_nodes:
                    write(f'EDGE\t{x}\t{y}')


def set_plot_labels(g, xlabel, ylabel, title, index_step=2, filter_ticks=True):
    g.set_ylabels(xlabel)
    g.set_xlabels(ylabel)
    g.ax.set_title(title)
    if filter_ticks:
        labels = g.ax.get_xticklabels() # get x labels
        g.ax.set_xticklabels((int(float(l.get_text())) if i%index_step == 1 else '' for i, l in enumerate(labels)))#, rotation=30)


def plot_number_per_score(data:{int: int}, countable:str, all_indexes:bool=True):
    data=transform_data_dict({k: len(v) for k, v in data.items()}, 'score', countable, all_indexes)
    g = sns.catplot(x="score", y=countable, data=data,
                    kind="bar", palette="muted")
    set_plot_labels(g, r'\# ' + countable, f"Cover (number of edges covered by the {countable})", f'Number of {countable} in {PRETTY_CASE_NAME}', 10 if all_indexes else 2)

    # save
    indexes = 'allindex_' if all_indexes else ''
    fig = f'out/number_{countable.replace(" ", "_").lower()}_per_score_{indexes}{CASE_NAME}.png'
    g.savefig(fig, dpi=300)
    print(f'Generated figure {fig}')

def plot_numbers_per_score(data1:{int: int}, countable1:str, data2:{int: int}, countable2:str, all_indexes:bool=False):
    data1 = {k: len(v) for k, v in data1.items()}
    data2 = {k: len(v) for k, v in data2.items()}
    df = pd.DataFrame({
        'score': tuple(data1) + tuple(data2),
        'type': tuple(countable1 for _ in data1) + tuple(countable2 for _ in data2),
        'number': tuple(v for v in data1.values()) + tuple(v for v in data2.values())
    })
    g = sns.catplot(x="score", y="number", hue="type", kind="bar", data=df)
    set_plot_labels(g, rf'\# {countable1} ~~~ \# {countable2}', f"Cover (number of edges covered by the concepts)", f'Number of {countable1} and {countable2} in {PRETTY_CASE_NAME}', 10 if all_indexes else 2)

    # save
    indexes = 'allindex_' if all_indexes else ''
    countable = '_'.join(c for c in (countable1, countable2))
    fig = f'out/number_{countable.replace(" ", "_").lower()}_per_score_{indexes}{CASE_NAME}.png'
    g.savefig(fig, dpi=300)
    print(f'Generated figure {fig}')


def transform_data_dict(data:dict, key:str, value:str, all_indexes:bool):
    if all_indexes:
        r = range(int(min(data)), int(max(data)) + 1)
        return pd.DataFrame({
            key: tuple(k for k in r),
            value: tuple(data.get(k, 0) for k in r)
        })
    else:
        k, v = zip(*data.items())
        return pd.DataFrame({key: tuple(k), value: tuple(v)})


if triplets and not args.no_plot:
    print('Plotting…')
    plot_number_per_score(triplets, 'Triplet Concept', False)
    plot_number_per_score(triplets, 'Triplet Concept', True)
    plot_number_per_score(concepts, 'Formal Concept', False)
    plot_number_per_score(concepts, 'Formal Concept', True)
    plot_numbers_per_score(triplets, 'Triplet Concept', concepts, 'Formal Concept')
elif triplets:
    print('Option --no-plot prevents to create graphics.')
else:
    print('No triplets, no graphics.')
print(f'Writing bubble in {CASE_PATHNAME_BBL}…')
write_bubble(triplets, search_stats)
