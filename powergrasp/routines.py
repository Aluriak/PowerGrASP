"""Definition of high level functions operating the compression.

"""

import csv
from .searchers import CliqueSearcher, BicliqueSearcher, StarSearcher, NonStarBicliqueSearcher
from .utils import get_time
from .graph import Graph
from .recipe import Recipe
from . import constants as const
from .constants import MULTISHOT_MOTIF_SEARCH, BUBBLE_FOR_EACH_STEP, TIMERS, SHOW_STORY, SHOW_DEBUG, STATISTIC_FILE, USE_STAR_MOTIF
from .motif_batch import MotifBatch
from multiprocessing.dummy import Pool as ThreadPool  # dummy here to use the threading backend, not process
from multiprocessing import Pool as ProcessPool


if TIMERS and STATISTIC_FILE:
    # function to fill the file during compression
    def save_stats(*args):
        """Fill statistic file with given data"""
        with open(STATISTIC_FILE, 'a') as fd:
            fd.write(','.join(map(str, args)) + '\n')


def search_best_motifs_sequentially(searchers, step, recipe) -> MotifBatch:
    """Return a MotifBatch instance containing the best motifs
    found by given searchers."""
    score_to_beat = 0
    best_motifs, best_motifs_score = None, 0
    ordered_searchers = const.MOTIF_TYPE_ORDER(searchers)
    for searcher in ordered_searchers:
        motifs = MotifBatch(searcher.search(step, score_to_beat, recipe=recipe))
        if motifs:
            searcher.on_new_found_motif(motifs)
            if motifs.score > best_motifs_score:
                best_motifs, best_motifs_score = motifs, motifs.score
                score_to_beat = best_motifs_score
    return best_motifs

def search_best_motifs_in_parallel(searchers, step, recipe) -> MotifBatch:
    """Return a MotifBatch instance containing the best motifs
    found by given searchers."""
    with ThreadPool(len(searchers)) as pool:
        founds = pool.starmap(search_best_motifs_sequentially, (([s], step, recipe) for s in searchers))
    return max(founds, key=lambda f: 0 if f is None else f.score)

if const.PARALLEL_MOTIF_SEARCH:
    search_best_motifs = search_best_motifs_in_parallel
else:
    search_best_motifs = search_best_motifs_sequentially


def compress(graph:Graph, *, cc_idx=None, recipe:[Recipe]=None) -> [str]:
    """Yield bubble lines found in graph"""
    if TIMERS:
        timer_start = get_time()
        timer_last = timer_start
    if USE_STAR_MOTIF:
        searchers = CliqueSearcher(graph), NonStarBicliqueSearcher(graph), StarSearcher(graph)
    else:
        searchers = CliqueSearcher(graph), BicliqueSearcher(graph)
    if SHOW_STORY:
        print('INFO searchers: ' + ', '.join(s.name for s in searchers))
        print(f"INFO recipe: {recipe}")
    recipe_lines, recipe_line, recipe_completed = iter(recipe or ()), None, False
    step = 0
    complete_compression = False
    while True:
        if recipe_line and recipe_line.isbreakable and not recipe_completed:
            pass  # reuse the same recipe line
        else:  # everything normal
            recipe_line = next(recipe_lines, None)
            recipe_completed = False
        if (SHOW_STORY and recipe_line) or SHOW_DEBUG: print('INFO recipe:', recipe_line)
        step += 1
        try:
            best_motifs = search_best_motifs(searchers, step, recipe=recipe_line)
        except KeyboardInterrupt:
            print('WARNING interrupted search. Graph compression aborted. Output will be written.')
            best_motifs = None
            break
        if best_motifs:  # let's compress it
            step += graph.compress_all(best_motifs.non_overlapping_subset())
            for searcher in searchers:
                searcher.on_new_compressed_motif(best_motifs)
            if BUBBLE_FOR_EACH_STEP:
                graph.output('out/out_k{}_s{}.bbl'.format(step, best_motif.score))
            if SHOW_STORY:
                print('INFO {} {} motif of score {} compressed'.format(best_motifs.count, best_motifs.name, best_motifs.score))
            if TIMERS:
                now = get_time()
                timers = round(now - timer_start, 2), round(now - timer_last, 2)
                if SHOW_STORY:
                    print("TIMER since start: {}s\t\tsince last motif: {}s"
                          "".format(*timers))
                timer_last = now
                for searcher in searchers:  # timer per motif search
                    timers = timers + ('{}:{}'.format(searcher.name, round(searcher.last_search_time, 2)),)
            if STATISTIC_FILE:
                bounds = [
                    '{}:[{};{}]'.format(searcher.name, searcher.lowerbound, searcher.upperbound)
                    for searcher in searchers
                ]
                if not TIMERS:
                    timers = 'none', 'none'
                save_stats(cc_idx, *timers, best_motifs.name, best_motifs.score, *bounds)
        else:
            if recipe_line:  # the recipe failed, or is optional
                recipe_completed = True
                if recipe_line.isbreakable:
                    if SHOW_DEBUG:
                        print(f"DEBUG breakable recipe {recipe_line} exhausted.")
                elif recipe_line.isrequired:
                    raise recipe_line.RecipeError(f"Recipe {recipe_line} failed, but was necessary.")
                else:  # it is optional
                    if SHOW_STORY:
                        print(f"INFO optional recipe {recipe_line} failed.")
            else:  # no recipe, so it's a normal ending of compression
                complete_compression = True
                break  # nothing to compress
        # finish compression if the recipe asks so (and is not an uncompleted breakable).
        if recipe_line and recipe_line.islast and not (recipe_line.isbreakable and not recipe_completed):
            break
    if TIMERS:
        timer_output = get_time()

    # write the bubble
    head_comment = ''
    if not complete_compression:
        head_comment = 'Warning: incomplete compression (stopped at step {})'.format(step)
    yield from graph.bubble_repr(head_comment=head_comment, given_uid=cc_idx)

    # timers
    if TIMERS:
        now = get_time()
        timers = round(now - timer_start, 2), round(now - timer_output, 2)
        if SHOW_STORY:
            print("TIMER since start: {}s\t\toutput generation: {}s"
                  "".format(*timers))

    # compute the statistics
    compression_statistics = tuple(graph.compression_metrics())
    if cc_idx:
        compression_statistics = (('connected component', cc_idx), *compression_statistics)
    if TIMERS:
        compression_statistics = (*compression_statistics, ('time since start', timers[0]))
    # write the statistics where available
    if const.CC_STATISTIC_FILE and cc_idx:
        with open(const.CC_STATISTIC_FILE, 'a') as fd:
            csv.writer(fd).writerow(v for _, v in compression_statistics)
    if const.BUBBLE_WITH_STATISTICS:
        yield from _gen_metrics(compression_statistics)


def compress_by_cc(fname:str, recipe_files:[str]=None) -> [str]:
    """Yield bubble lines from compression of each cc found in given filename

    recipe_files -- iterable of filenames or raw recipe, or Recipe objects

    """
    if TIMERS and const.BUBBLE_WITH_STATISTICS:
        timer = get_time()
    if recipe_files:
        if SHOW_STORY:
            print('INFO recipe files:', recipe_files)
        recipe_files = tuple([recipe_files] if isinstance(recipe_files, str) else recipe_files)
        recipes = tuple(map(Recipe.from_, recipe_files))
        def recipe_for(graph:Graph, recipes=recipes) -> Recipe:
            "Return the first recipe using a node found in given graph"
            for recipe in recipes:
                if recipe.works_on(graph):
                    return recipe
    else:
        def recipe_for(*_, **__): return None  # no recipe available

    graphs = enumerate(Graph.ccs_from_file(fname), start=1)
    stats = None
    if const.PARALLEL_CC_COMPRESSION == 1:  # simple case, allowing for global stats
        for idx, graph in graphs:
            if idx > 1:  yield ''
            yield '# CONNECTED COMPONENT {}'.format(idx)
            yield from compress(graph, cc_idx=idx, recipe=recipe_for(graph))
            if const.GLOBAL_STATISTICS:
                stats = _build_global_stats(stats, graph.compression_metrics_data())
    else:  # many processes imply a more complex system
        nb_process = const.PARALLEL_CC_COMPRESSION
        if nb_process == 0:
            graphs = ((idx, gr, recipe_for(gr)) for idx, gr in graphs)
            graphs = tuple(graphs)  # RIP memory
            nb_process = len(graphs) or 1
        with ProcessPool(nb_process) as pool:
            for lines, stats_data in pool.starmap(_func_on_graph, graphs):
                yield from lines
                if const.GLOBAL_STATISTICS:
                    stats = _build_global_stats(stats, stats_data)

    # show global stats
    if stats is not None and const.BUBBLE_WITH_STATISTICS:
        yield '# TOTAL GRAPH METRICS'
        yield from _gen_metrics(Graph.compression_metrics_from_data(stats))
    if TIMERS and const.BUBBLE_WITH_STATISTICS:
        yield '# total compression time: {}'.format(round(get_time() - timer, 2))


def _func_on_graph(idx, graph, recipe):
    """Function used by multiprocessing compression of cc. Needs to be global
    to be pickled."""
    lines = (
        '# CONNECTED COMPONENT {}'.format(idx),
        *compress(graph, cc_idx=idx, recipe=recipe)
    )
    return lines, graph.compression_metrics_data()


def _build_global_stats(prev:tuple, current:tuple):
    """Return the addition of previous and current statistics values"""
    if prev is None:
        return current
    return tuple(one + two for one, two in zip(prev, current))


def _gen_metrics(metrics:[(str, float)]) -> str:
    """Yield lines describing given iterable of metric and their value."""
    metrics = tuple(metrics)
    metric_name_size = max((len(m) for m, _ in metrics))
    for metric, value in metrics:
        if isinstance(value, float): value = round(value, 2)
        yield '# {}: {}'.format(metric.ljust(metric_name_size), value)
