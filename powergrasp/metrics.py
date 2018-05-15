def conversion_rate(initial_edge, final_edge, poweredge, powernode):
    """Compute conversion rate"""
    try:
        edge = initial_edge
        poweredge = final_edge + poweredge
        return (edge - poweredge) / powernode
    except ZeroDivisionError:
        return 1.

def edge_reduction(initial_edge, final_edge, poweredge, _):
    """Compute edge reduction (percentage)"""
    try:
        edge = initial_edge
        poweredge = final_edge + poweredge
        return ((edge - poweredge) / edge) * 100
    except ZeroDivisionError:
        return 100.

def compression_ratio(initial_edge, final_edge, poweredge, _):
    """Compute data compression ratio"""
    try:
        return initial_edge / (final_edge + poweredge)
    except ZeroDivisionError:
        return 1.


def compression_metrics(initial_edge, final_edge, poweredge, powernode) -> [(str, float)]:
    """Yield pairs (name, value) describing measures and their value.

    initial_edge -- number of edge in initial graph
    final_edge -- number of (non power) edge in final graph
    poweredge -- number of poweredge in final graph
    powernode -- number of powernode in final graph

    """
    payload = initial_edge, final_edge, poweredge, powernode
    for func in (conversion_rate, edge_reduction, compression_ratio):
        yield func.__name__.replace('_', ' '), func(*payload)
