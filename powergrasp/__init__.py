import importlib.resources

ASP_FILES = {
    fname: importlib.resources.files(__name__).joinpath('asp/' + fname + '.lp')
    for fname in ('search-triplet', 'search-fullbiclique', 'search-biclique', 'search-quasibiclique', 'search-star', 'search-clique', 'process-motif', 'block-constraint-cpu', 'block-constraint-memory', 'scoring_powergraph')
}

from .routines import compress_by_cc

__version__ = '0.8.19.dev0'
