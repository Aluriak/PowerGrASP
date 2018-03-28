
import clyngor
from constants import COVERED_EDGES_FROM_ASP, SHOW_STORY


def solve_motif_search(step:int, lowerbound:int, upperbound:int, files:iter, graph:str) -> iter:
    """Return atoms found in best model"""
    constants = {'k': step, 'lowerbound': lowerbound, 'upperbound': upperbound}
    if COVERED_EDGES_FROM_ASP:
        constants['covered_edges_from_asp'] = 1
    models = clyngor.solve(files=tuple(files), inline=str(graph), constants=constants, stats=False)

    if SHOW_STORY:
        print('SOLVE', models.command)

    model = None
    for model in models.by_predicate.careful_parsing:
        pass  # get the last one
    return model
