"""Some constants to tune the compression behavior.

Mostly used for dev and debug.

"""
import os
import json

# Default values
constants = {
    # Run some integrity tests at some points. May slow the compression a lot.
    'TEST_INTEGRITY': True,

    # Show main steps of the compression.
    'SHOW_STORY': True,

    # Show motifs transformation into powergraph.
    'SHOW_MOTIF_HANDLING': False,

    # Show full trace of the compression. Useful for debugging.
    'SHOW_DEBUG': False,

    # Recover covered edges from ASP. If falsy, will ask motif searcher to compute the edges, which may be quicker.
    'COVERED_EDGES_FROM_ASP': False,

    # Nodes and sets are optional in the output bubble.
    'BUBBLE_WITH_NODES': True,
    'BUBBLE_WITH_SETS': True,

    # Edges in bubble are associated to a factor
    'BUBBLE_POWEREDGE_FACTOR': '1.0',
    'BUBBLE_EDGE_FACTOR': '1.0',

    # When possible, delete the quotes around identifiers in the bubble. May lead to node name collision.
    'BUBBLE_SIMPLIFY_QUOTES': True,

    # Change them according to config file
    'CONFIG_FILE': 'powergrasp.cfg',

    # Search for multiple motif in a single search. Accelerate the solving for graph with lots of equivalent motifs.
    'MULTISHOT_MOTIF_SEARCH': False,
}


try:
    with open(constants['CONFIG_FILE']) as fd:
        cfg = json.load(fd)
        for field, value in cfg.items():
            field = field.upper().replace(' ', '_')
            if field in constants:
                constants[field] = value
        print('INFO: config file {} loaded.'.format(fd.name))
except FileNotFoundError:
    if constants['SHOW_STORY'] or constants['SHOW_DEBUG']:
        print("INFO no config file")


# Put them in global access
for field, value in constants.items():
    globals()[field] = value
