import pkg_resources
ASP_FILES = {
    fname: pkg_resources.resource_filename(__name__, 'asp/' + fname + '.lp')
    for fname in ('search-biclique', 'search-clique', 'process-motif', 'scoring_powergraph')
}

from .routines import compress_by_cc
