"""Some constants to tune the compression behavior.

Final user may want to override it by writing in 'powergrasp.cfg' file in
either JSON or INI format.

"""
import os
import json
import configparser
import multiprocessing
from collections import ChainMap

# Default values
constants = {
    # Run some integrity tests at some points. May slow the compression a lot.
    'TEST_INTEGRITY': True,

    # Show main steps of the compression.
    'SHOW_STORY': True,

    # Show motifs transformation into powergraph.
    'SHOW_MOTIF_HANDLING': False,

    # Timers.
    'TIMERS': True,

    # Statistics file to write during compression.
    'STATISTIC_FILE': None,

    # Generate and save a bubble representation of the graph at each step.
    'BUBBLE_FOR_EACH_STEP': False,

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
    'MULTISHOT_MOTIF_SEARCH': True,

    # Optimization on biclique lowerbound computation. Can be costly. Deactivate with 1. With value at n, up to n neighbors are considered.
    'BICLIQUE_LOWERBOUND_MAXNEI': 2,

    # Number of CPU available to clingo (or a string like '2,join' or '48,compete'), or 0 for autodetect number of CPU.
    'CLINGO_MULTITHREADING': 1,

    # When a choice is given, prefer memory over CPU:
    'OPTIMIZE_FOR_MEMORY': False,

    # TODO  Detect and postpone compression of terminal tree subgraphs
    'TERMINAL_TREES_POSTPONING': True,
    # TODO  Detect, delete and restore bridges
    'BRIDGES_CUT': True,
    # TODO  Detect and if available run specialized compression routine for: trees, triangle-free graphs, cactii.
    #  Will not do anything on a graph that does not belong to those classes.
    'SPECIAL_CASES_DETECTION': True,
}


def open_config_file(fname:str) -> dict:
    """Try reading file in INI, and if it do not works, try JSON"""
    try:
        # read file, take all available sections
        config = configparser.ConfigParser()
        config.read(fname)
        if not config.sections():
            print('ERROR input config do not have any section.')
        else:
            return {
                key: config[section][key]
                for section in config.sections()
                for key in config[section]
            }
    except configparser.MissingSectionHeaderError as err:
        ini_err = err.args[0]
        try:
            with open(fname) as fd:
                return json.load(fd)
        except json.decoder.JSONDecodeError as err:
            json_err = err.args[0]
            print("ERROR input config file is not a valid json, nor a valid ini."
                  "\nINI  error: {}\nJSON error: {}".format(ini_err, json_err))


try:
    cfg = open_config_file(constants['CONFIG_FILE'])
except FileNotFoundError:
    cfg = None
if cfg:
    for field, value in cfg.items():
        field = field.upper().replace(' ', '_')
        if field in constants:
            constants[field] = value
    if constants['SHOW_STORY'] or constants['SHOW_DEBUG']:
        print('INFO: config file {} loaded.'.format(constants['CONFIG_FILE']))
elif constants['SHOW_STORY'] or constants['SHOW_DEBUG']:
    print("INFO no config file")


def _convert_parallel_mode_option(value:str or int) -> str:
    """Return the option to give to clingo to handle given number of CPU.

    >>> _convert_parallel_mode_option(0)
    ' --parallel-mode=4'
    >>> _convert_parallel_mode_option(1)
    ''
    >>> _convert_parallel_mode_option('2')
    ' --parallel-mode=2'
    >>> _convert_parallel_mode_option('0,join')
    ' --parallel-mode=4,join'

    """
    if isinstance(value, str):
        if value.isnumeric():
            return str(_convert_parallel_mode_option(int(value)))
        if value and value.startswith('0'):
            nb_cpu = str(multiprocessing.cpu_count())
            return _convert_parallel_mode_option(nb_cpu + value.lstrip('0'))
        elif value:
            return ' --parallel-mode=' + value
    elif value == 0:
        return _convert_parallel_mode_option(multiprocessing.cpu_count())
    elif value > 1:
        return ' --parallel-mode=' + str(value)
    return ''


# Apply the value convertion, if any.
_CONVERTIONS = {
    'CLINGO_MULTITHREADING': _convert_parallel_mode_option,
    'BICLIQUE_LOWERBOUND_MAXNEI': int,
}
constants = {f: _CONVERTIONS.get(f, lambda x:x)(v) for f, v in constants.items()}


# Put them in global access
globals().update(constants)
