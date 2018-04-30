"""Some constants to tune the compression behavior.

Final user may want to override it by writing in 'powergrasp.cfg' file in
either JSON or INI format.

"""
import os
import ast
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

    # Prefix to add to all (power)nodes names in output.
    'OUTPUT_NODE_PREFIX': '',

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

    # Optimization on biclique lowerbound computation. Can be costly. Deactivate with 2. With value at n, up to n neighbors are considered.
    'BICLIQUE_LOWERBOUND_MAXNEI': 2,

    # Arbitrary parameters to give to clingo (note that some, like multithreading or optmode, may already be set by other options).
    'CLINGO_OPTIONS': {},

    # Number of CPU available to clingo (or a string like '2,join' or '48,compete'), or 0 for autodetect number of CPU.
    'CLINGO_MULTITHREADING': 1,

    # Two different motifs for stars and bicliques, so the work of biclique is lighter.
    'USE_STAR_MOTIF': True,

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


def make_key(key:str) -> str:
    """Return the well formed key for constants dictionary"""
    return key.upper().replace(' ', '_')

def make_value_from_ini(key:str, section, config:configparser.ConfigParser):
    """Return the int, str, dict, float or tuple equivalent to value
    found for given section and key.

    """
    assert key in constants, key
    assert section in config
    assert key in config[section], (config[section], key)
    default = constants[key]
    if isinstance(default, bool):
        return config.getboolean(section, key)
    elif isinstance(default, (int, float, tuple, list, dict, set, frozenset, type(None))):
        try:
            return type(default)(ast.literal_eval(config[section][key]))
        except ValueError as err:  # it's not a python literal, so it's a string
            return config[section][key]
    elif isinstance(default, str):
        return config[section][key]
    else:
        raise ValueError("Non-handled option type {} for field {}"
                         "".format(type(default), key))

def open_config_file(fname:str) -> dict:
    """Try reading file in INI, and if it do not works, try JSON"""
    try:
        # read file, take all available sections
        config = configparser.ConfigParser()
        config.read(fname)
        if config.sections():
            return {
                key: make_value_from_ini(key, section, config)
                for section in config.sections()
                for key in map(make_key, config[section])
            }
        else:
            print('ERROR input config do not have any section.')
    except configparser.MissingSectionHeaderError as err:
        ini_err = err.args[0]
        try:
            with open(fname) as fd:
                return {make_key(k): v for k, v in json.load(fd).items()}
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
        if field in constants:
            constants[field] = value
        elif constants['SHOW_STORY'] or constants['SHOW_DEBUG']:
            raise ValueError("field '{}' is not a valid field for configuration."
                             "".format(field))
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
    >>> _convert_parallel_mode_option(' 2')
    ' --parallel-mode=2'
    >>> _convert_parallel_mode_option('0,split')
    ' --parallel-mode=4,split'
    >>> _convert_parallel_mode_option("'0,split'")
    ' --parallel-mode=4,split'
    >>> _convert_parallel_mode_option('"0,split"')
    ' --parallel-mode=4,split'

    """
    if isinstance(value, str):
        value = value.strip(' "\'\t\n')
        if value.isnumeric():
            return str(_convert_parallel_mode_option(int(value)))
        elif value and value.startswith('0'):
            if value[1:] not in {',compete', ',split'}:
                raise ValueError("Multithreading option value is not valid: {}"
                                 "".format(value))
            nb_cpu = str(multiprocessing.cpu_count())
            return _convert_parallel_mode_option(nb_cpu + value.lstrip('0'))
        elif value:
            return ' --parallel-mode=' + value
    elif value == 0:
        return _convert_parallel_mode_option(multiprocessing.cpu_count())
    elif value > 1:
        return ' --parallel-mode=' + str(value)
    return ''


def _convert_clingo_options(value:dict or str) -> dict:
    """Return a map from motif name to clingo options."""
    # NB: can't access MotifSearchers subclass at this point, since constants
    #  are computed at import time. We therefore can't verify the keys of the dict.
    # convert string to dict
    if isinstance(value, str):
        value = {None: value}
    # validate and return the dict
    value = {None if motif is None else motif.lower().replace(' ', '-').replace('_', '-'): options
             for motif, options in value.items()}
    value.setdefault(None, '')
    return value


# Apply the value convertion, if any.
_CONVERTIONS = {
    'CLINGO_MULTITHREADING': _convert_parallel_mode_option,
    'BICLIQUE_LOWERBOUND_MAXNEI': int,
    'CLINGO_OPTIONS': _convert_clingo_options,
}
constants = {f: _CONVERTIONS.get(f, lambda x:x)(v) for f, v in constants.items()}

# verifications about clingo options
if constants['CLINGO_MULTITHREADING']:
    for motif, options in constants['CLINGO_OPTIONS'].items():
        if '--parallel-mode=' in options:
            raise ValueError("Invalid option value: --parallel-mode given by both"
                             " CLINGO_OPTIONS ({}) and CLINGO_MULTITHREADING ({})."
                             "".format(options, constants['CLINGO_MULTITHREADING']))


# Put them in global access
globals().update(constants)
