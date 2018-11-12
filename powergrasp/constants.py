"""Some constants to tune the compression behavior.

Final user may want to override it by writing in 'powergrasp.cfg' file in
either JSON or INI format.

"""
import os
import ast
import json
import itertools
import configparser
import multiprocessing
from collections import ChainMap
from . import utils

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

    # Connected components statistics file to write at the end of each cc.
    'CC_STATISTIC_FILE': None,

    # Compute statistics/metrics over all connected components.
    'GLOBAL_STATISTICS': True,

    # Include some statistics in output bubble.
    'BUBBLE_WITH_STATISTICS': True,

    # Generate and save a bubble representation of the graph at each step.
    'BUBBLE_FOR_EACH_STEP': False,

    # Keep simple edges in output.
    'BUBBLE_WITH_SIMPLE_EDGES': True,

    # Prefix to add to all (power)nodes names in output.
    'OUTPUT_NODE_PREFIX': '',

    # Show full trace of the compression. Useful for debugging.
    'SHOW_DEBUG': False,

    # Recover covered edges from ASP. If falsy, will ask motif searcher to compute the edges, which may be quicker.
    'COVERED_EDGES_FROM_ASP': False,

    # Nodes and sets are optional in the output bubble.
    'BUBBLE_WITH_NODES': True,
    'BUBBLE_WITH_SETS': True,

    # Put each connected component in a dedicated powernode.
    'BUBBLE_EMBEDS_CC': False,

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

    # When a choice is given, prefer memory over CPU.
    'OPTIMIZE_FOR_MEMORY': False,

    # If set, will keep nodes connected to nothing. Else, will discard them.
    'KEEP_SINGLE_NODES': True,

    # Ignore edges dynamically determined as impossible to compress.
    'GRAPH_FILTERING': True,

    # Perform the search for motifs in different process instead of sequentially.
    'PARALLEL_MOTIF_SEARCH': False,

    # Number of processes to work on connected components. Zero to get one per cc. One to deactivate.
    'PARALLEL_CC_COMPRESSION': 1,

    # Define in which order the motifs are tested.
    'MOTIF_TYPE_ORDER': 'star,clique,non-star-biclique,biclique',

    # TODO  Detect and postpone compression of terminal tree subgraphs
    # 'TERMINAL_TREES_POSTPONING': True,
    # TODO  Detect, delete and restore bridges
    # 'BRIDGES_CUT': True,
    # TODO  Detect and if available run specialized compression routine for: trees, triangle-free graphs, cactii.
    #  Will not do anything on a graph that does not belong to those classes.
    # 'SPECIAL_CASES_DETECTION': True,
}

_derived_constants = {
    'KEEP_NX_GRAPH': lambda c: c['GRAPH_FILTERING'],
}


def make_key(key:str) -> str:
    """Return the well formed key for constants dictionary"""
    return key.upper().replace(' ', '_')

def make_value_from_ini(found_key:str, real_key:str, section,
                        config:configparser.ConfigParser):
    """Return the int, str, dict, float or tuple equivalent to value
    found for given section and key.

    """
    assert real_key in constants, f"{real_key} key found in config file is unexpected"
    assert section in config
    assert found_key in config[section], (config[section], found_key)
    default = constants[real_key]
    if isinstance(default, bool):
        return config.getboolean(section, found_key)
    elif isinstance(default, type(None)):
        try:
            return ast.literal_eval(config[section][found_key])
        except ValueError as err:  # it's not a python literal, so it's a string
            return config[section][found_key]
    elif isinstance(default, (int, float, tuple, list, dict, set, frozenset)):
        value = config[section][found_key] or '""'  # cast empty value to empty string
        try:
            return type(default)(ast.literal_eval(value))
        except ValueError as err:  # it's not a python literal, so it's a string
            return config[section][found_key]
    elif isinstance(default, str):
        return config[section][found_key]
    else:
        raise ValueError("Non-handled option type {} for field {}"
                         "".format(type(default), real_key))

def open_config_file(fname:str) -> dict:
    """Try reading file in INI, and if it do not works, try JSON"""
    try:
        # read file, take all available sections
        config = configparser.ConfigParser()
        config.read(fname)
        if config.sections():
            return {
                key: make_value_from_ini(found_key, key, section, config)
                for section in config.sections()
                for found_key, key in map(lambda k:(k, make_key(k)), config[section])
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


def _convert_motif_type_order(value:str) -> callable:
    """Return a function returning sorted searchers according to the given value.

    For instance, if input is 'worst-upperbound-first', the function returned
    will sort input searchers according to their upperbound, smallest first.

    """
    error = lambda m: ValueError("Invalid value for option MOTIF TYPE ORDER: {} ({})".format(value, m))
    value = value.lower().replace(' ', '-').replace('_', '-')
    if ',' in value:
        order = {name: idx for idx, name in enumerate(map(str.strip, value.split(',')))}
        def ordered(searchers, *, order=order) -> iter:
            """Yield given searchers according to their priority"""
            return sorted(searchers, key=lambda s: order[s.name])
    elif '-' in value:
        which, bound, where = value = value.split('-')
        greatests = {'greatest', 'biggest'}
        smallests = {'worst', 'smallest'}
        if len(value) != 3:
            raise error("{} groups instead of 3, like 'greatest-lowerbound-first'".format(len(value)))
        if which not in greatests | smallests:
            raise error("the which value must be something like worst or greatest".format(len(value)))
        reverse = (where == 'first') != (which in smallests)
        if bound == 'lowerbound':
            key = lambda s: s.lowerbound
        elif bound == 'upperbound':
            key = lambda s: s.upperbound
        else:
            raise error("the bound value must be upperbound or lowerbound".format(len(value)))
        def ordered(searchers, *, reverse=reverse, key=key) -> iter:
            return sorted(searchers, reverse=reverse, key=key)
    elif value == 'random':  # funny, but not really useful
        def ordered(searchers) -> iter:
            import random
            searchers = list(searchers)
            random.shuffle(searchers)
            return searchers
    else:
        raise error("not a list of elements or groups, like 'star,clique,non-star-biclique,biclique' or 'greatest-lowerbound-first'")
    return ordered

def _convert_erased_file(fname:str) -> str:
    """A type to give to convertion, where value is a file to erase."""
    if fname is not None:
        with open(fname, 'w') as fd:
            pass  # just erase it
    return fname  # conserve it untouched


# Apply the value convertion, if any.
_CONVERTIONS = {
    'CLINGO_MULTITHREADING': _convert_parallel_mode_option,
    'BICLIQUE_LOWERBOUND_MAXNEI': int,
    'CLINGO_OPTIONS': _convert_clingo_options,
    'MOTIF_TYPE_ORDER': _convert_motif_type_order,
    'CC_STATISTIC_FILE': _convert_erased_file,
    'COMPRESSION_STATISTIC_FILE': _convert_erased_file,
    'STATISTIC_FILE': _convert_erased_file,
}
constants = {f: _CONVERTIONS.get(f, lambda x:x)(v) for f, v in constants.items()}
# add the derived ones
constants.update({
    field: make_value(constants)
    for field, make_value in _derived_constants.items()
})

# verifications about clingo options
if constants['CLINGO_MULTITHREADING']:
    for motif, options in constants['CLINGO_OPTIONS'].items():
        if '--parallel-mode=' in options:
            raise ValueError("Invalid option value: --parallel-mode given by both"
                             " CLINGO_OPTIONS ({}) and CLINGO_MULTITHREADING ({})."
                             "".format(options, constants['CLINGO_MULTITHREADING']))


# Put them in global access
globals().update(constants)


def print_config():
    """Print configuration in stdout"""
    # name_width = max(len(name) for name, _ in uplets)
    # value_width = max(len(repr(value)) for _, value in uplets)
    uplets = sorted(tuple(OPTIONS_CATEGORIES.items()))
    name_width = max(len(name) for _, names in uplets for name in names)
    for category, options in uplets:
        print('[{}]'.format(category))
        for option in options:
            value = repr(constants[option]).strip('"\'')
            option = option.lower().replace('_', ' ').ljust(name_width)
            print('{} = {}'.format(option, value))
        print()



OPTIONS_CATEGORIES = utils.reverse_dict({
    'TEST_INTEGRITY': 'debug',
    'SHOW_STORY': 'debug',
    'SHOW_MOTIF_HANDLING': 'debug',
    'TIMERS': 'statistics',
    'STATISTIC_FILE': 'statistics',
    'CC_STATISTIC_FILE': 'statistics',
    'GLOBAL_STATISTICS': 'statistics',
    'BUBBLE_WITH_STATISTICS': 'statistics',
    'BUBBLE_FOR_EACH_STEP': 'debug',
    'BUBBLE_WITH_SIMPLE_EDGES': 'output',
    'OUTPUT_NODE_PREFIX': 'output',
    'SHOW_DEBUG': 'debug',
    'COVERED_EDGES_FROM_ASP': 'optimization',
    'BUBBLE_WITH_NODES': 'output',
    'BUBBLE_WITH_SETS': 'output',
    'BUBBLE_POWEREDGE_FACTOR': 'output',
    'BUBBLE_EDGE_FACTOR': 'output',
    'BUBBLE_EMBEDS_CC': 'output',
    'BUBBLE_SIMPLIFY_QUOTES': 'input',
    'CONFIG_FILE': 'input',
    'MULTISHOT_MOTIF_SEARCH': 'optimization',
    'BICLIQUE_LOWERBOUND_MAXNEI': 'optimization',
    'CLINGO_OPTIONS': 'clingo',
    'CLINGO_MULTITHREADING': 'clingo',
    'USE_STAR_MOTIF': 'optimization',
    'OPTIMIZE_FOR_MEMORY': 'optimization',
    'KEEP_SINGLE_NODES': 'output',
    'KEEP_NX_GRAPH': 'optimization',
    'GRAPH_FILTERING': 'optimization',
    'PARALLEL_MOTIF_SEARCH': 'optimization',
    'PARALLEL_CC_COMPRESSION': 'optimization',
    'MOTIF_TYPE_ORDER': 'optimization',
    'CC_STATISTIC_FILE': 'statistics',

    # 'TERMINAL_TREES_POSTPONING': 'optimization',
    # 'BRIDGES_CUT': 'optimization',
    # 'SPECIAL_CASES_DETECTION': 'optimization',
})
categorized_options = frozenset(itertools.chain.from_iterable(OPTIONS_CATEGORIES.values()))
assert all(option in constants for option in categorized_options)
for constant in constants:
    if constant not in categorized_options:
        raise ValueError("Option {} has no category".format(constant))
