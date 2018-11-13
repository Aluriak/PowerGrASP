
import re
import math
import time
import phasme


def get_time() -> float: return time.time()



def maximal_clique_size(nb_edge:int) -> int:
    """Maximal number of nodes implied in a clique when there is given
    number of edges between neighbors of a node.

    nb_edge -- number of edges between neighbors of a node n
    return -- maximal number of node implied in a clique implying node n

    The number of edges covered by a clique of n nodes is given by function k:
    k(n) = n(n-1) / 2

    The contraposition of k, giving the number of nodes n in a clique of k(n) edges is:
    n = (1 + √(1+8*k(n))) / 2

    Proof: function k may be expressed as:
    n^2 - n - 2k(n) = 0
    The discriminant Δ = (-1)^2 - 4 * 1 * (-2k(n)) = 1 + 8k(n)
    Roots are (1±√Δ)/2, only the positive one is relevant (unless antimatter is involved),
    therefore root of k is (1 + √(1+8*k(n))) / 2               □

    For any node n, the maximal clique MC implying node n is constitued of n
    and its neighbors having a link between them.
    An upperbound of that number of node is given by
    considering that neighbors link are optimally placed to create a clique.

    There is therefore, in the best case, NMC(n) nodes in the maximal
    clique implying n:
    NMC(n) = 1 + ⌊ (1 + √(1+8*v(n))) / 2 ⌋

    With v(n) the number of edges between the neighbors of n.

    NMC(n) may then be used to compute the upperbound of clique search,
    by taking the maximal NMC(n) for all n of the graph in which a clique
    is searched.

    >>> maximal_clique_size(0)  # when no edge between neighbors: the node and one neighbor make the clique
    2
    >>> maximal_clique_size(1)  # when 1 edge between neighbors of n, the maximal clique imply two neighbors and n
    3
    >>> maximal_clique_size(2)  # when 2 edges between neighbors of n, the maximal clique imply two neighbors and n
    3
    >>> maximal_clique_size(3)
    4
    >>> maximal_clique_size(4)
    4
    >>> maximal_clique_size(5)
    4
    >>> maximal_clique_size(6)
    5

    """
    return 1 + int((1 + math.sqrt(1 + 8 * nb_edge)) / 2)


def quoted(string:str) -> str:
    """Return the given string, quoted, and with internal quotes escaped.

    Existing quotes will be escaped.

    >>> quoted('a')
    '"a"'
    >>> quoted('"a"')
    '"\\\\"a\\\\""'
    >>> quoted('"a')
    '"\\\\"a"'

    """
    # space is here to allow the regex to match for the first char
    return '"' + re.sub(r'([^\\])"', r'\1\\"', ' ' + string)[1:] + '"'


def unquoted(string:str) -> str:
    """Return the given string, unquoted.

    >>> unquoted('a')
    'a'
    >>> unquoted('"a"')
    'a'
    >>> unquoted('"a')
    '"a'

    """
    if string[0] == '"' and string[-1] == '"':
        return string[1:-1]
    return string


def normalized_name(string:str) -> str:
    """Return the normalized string, that consist of a quoted string
    with special characters replaced by their ord number.

    >>> normalized_name('a')
    '"a"'
    >>> normalized_name('A')
    '"A"'
    >>> normalized_name('"a"')
    '"a"'
    >>> normalized_name('"a')
    '"_c34_a"'

    """
    return quoted(phasme.commons.fixed_name(unquoted(string)))


def reverse_dict(indict:dict) -> dict:
    """Return a dict containing values of input dict as keys,
    and a set of associated keys as values.

    >>> reverse_dict({1: 2, 3: 2})
    {2: {1, 3}}
    >>> reverse_dict({1: 2, 3: 4})
    {2: {1}, 4: {3}}

    """
    ret = {}
    for key, val in indict.items():
        ret.setdefault(val, set()).add(key)
    return ret
