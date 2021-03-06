import pkg_resources
ASP_FILES = {
    fname: pkg_resources.resource_filename(__name__, 'asp/' + fname + '.lp')
    for fname in ('search-triplet', 'search-fullbiclique', 'search-biclique', 'search-quasibiclique', 'search-star', 'search-clique', 'process-motif', 'block-constraint-cpu', 'block-constraint-memory', 'scoring_powergraph')
}

from .routines import compress_by_cc

__version__ = '0.8.19.dev0'
