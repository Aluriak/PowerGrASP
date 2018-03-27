
import clyngor


def solve_motif_search(step:int, lowerbound:int, upperbound:int, files:iter, graph:str) -> iter:
    """Return atoms found in best model"""
    constants = {'k': step, 'lowerbound': lowerbound, 'upperbound': upperbound}
    models = clyngor.solve(files=tuple(files), inline=str(graph), constants=constants)
    print('SOLVE', models.command)

    model = None
    for model in models.by_predicate.careful_parsing:
        pass  # get the last one
    return model
