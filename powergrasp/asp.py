"""Search for motif using clyngor/clingo/ASP.

Function solve_motif_search is defined according to global constants.

"""

import math
import clyngor
from powergrasp.constants import (COVERED_EDGES_FROM_ASP, SHOW_STORY, SHOW_DEBUG,
                                  MULTISHOT_MOTIF_SEARCH, CLINGO_MULTITHREADING)


def _build_solver(step:int, lowerbound:int, upperbound:int, files:iter, graph:str, options:str) -> iter:
    """Return iterator over found models"""
    constants = {'k': step, 'lowerbound': lowerbound, 'upperbound': upperbound}
    if COVERED_EDGES_FROM_ASP:
        constants['covered_edges_from_asp'] = 1
    options += CLINGO_MULTITHREADING
    models = clyngor.solve(files=tuple(files), inline=str(graph), constants=constants, stats=False, options=options)
    if SHOW_STORY:
        print('SOLVE', models.command)
    return models.by_predicate.careful_parsing


def oneshot_motif_search(step:int, lowerbound:int, upperbound:int, files:iter, graph:str, options:str='') -> iter:
    """Return iterable over the generator of the one best model
    containing atoms found in best model"""
    model = None
    for model in _build_solver(step, lowerbound, upperbound, files, graph, options):
        pass  # get the last one
    if model:
        yield model


def multishot_motif_search(step:int, lowerbound:int, upperbound:int, files:iter, graph:str, options:str='') -> iter:
    """Yield atoms found in bests models"""
    all_models = _build_solver(step, lowerbound, upperbound, files, graph, options='--opt-mode=optN ' + options)
    best_opt, models = math.inf, []
    for model, opt in all_models.with_optimization:
        if SHOW_DEBUG:
            print('OPT, MODEL:', opt[0], model)
        if opt[0] < best_opt:  # smaller is best
            best_opt, models = opt[0], []  # model will be given again as last model, so no need to include it twice
        else:
            models.append(model)
    yield from models


# define the default behavior
if MULTISHOT_MOTIF_SEARCH:
    solve_motif_search = multishot_motif_search
else:
    solve_motif_search = oneshot_motif_search
