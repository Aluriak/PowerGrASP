"""Create a table of triplet state combinations"""


import itertools
CROSS = r'\x'
EMPTY = r'  '

A_CASES, B_CASES, C_CASES = (0, 1, 2), (0, 1, 2), (0, 1, 2)
COLSEP = '&'


def nb_edge_of(a, b, c):
    return int(a * b + a * c + b * c + (c*(c-1))/2)
def is_canonical(a, b, c):
    if a == 1 or b == 1:
        return False
    if (not a) and b:  # a empty, but not b
        return False
    return nb_edge_of(a, b, c) > 0

def desc_other_forms(a, b, c):
    P002 = '$7$', 'equivalent to $A=0, B=0, C=2$'
    if nb_edge_of(a, b, c) == 0:  return
    if a == 0 and b == 0:
        if c == 2:
            return r'$1+\frac{|C|!}{(|C|-2)!}+2\times |C|$', r'\newline$\forall x,y \in C$: $A=\{x\} \land B=\{y\}$'  # permutation writing
        elif c == 1:
            return r'$3$', r'$A=\{x\} or B=\{x\} or C=\{x\}$'
    elif a == 0:
        if b == 1:
            return P002
        else:
            assert b == 2
            if c == 1:
                return r'$2 \times 2$', 'move $C$ in $A$ and $A\leftrightharpoons B$'
            elif c == 2:
                return r'$1 + |C| \times 2$', 'move $c\in C$ in $A$ and $A\leftrightharpoons B$'
    elif b == 0:
        if a == 1:
            return P002
        else:
            assert a == 2
            if c == 1:
                return r'$2 \times 2$', 'move $C$ in $B$ and $A\leftrightharpoons B$'
            elif c == 2:
                return r'$1 + |C| \times 2$', 'move $c\in C$ in $B$ and $A\leftrightharpoons B$'
    if a == 1 and b == 1:
        if c == 0:
            return P002
        elif c == 1:
            return P002
        else:
            return P002
    elif a == 1:
        assert b == 2
        return r'2', r'$A=\emptyset \land C=C\cup A$'
    elif b == 1:
        assert a == 2
        return r'2', r'$B=\emptyset \land C=C\cup B$'
    elif a == 2 and b == 2:
        return r'2', r'$A\leftrightharpoons B$'
    assert False, f'MISSING CASE: ({a}, {b}, {c})'

columns = {
    r'$A_0$': lambda a, b, c: a == 0,
    r'$A_1$': lambda a, b, c: a == 1,
    r'$A_{2+}$': lambda a, b, c: a == 2,
    r'$B_0$': lambda a, b, c: b == 0,
    r'$B_1$': lambda a, b, c: b == 1,
    r'$B_{2+}$': lambda a, b, c: b == 2,
    r'$C_0$': lambda a, b, c: c == 0,
    r'$C_1$': lambda a, b, c: c == 1,
    r'$C_{2+}$': lambda a, b, c: c == 2,
    # 'has edge': lambda a, b, c: nb_edge_of(a, b, c) > 0,
    # 'canonical': is_canonical,
    'edge': lambda a, b, c: nb_edge_of(a, b, c) > 0,
    'can.': is_canonical,
    r'\# of form': desc_other_forms,
}
def render_desc_other_forms(segments):
    if segments is None: return ''  # 'no edges'  # clearer when empty ?
    return ' $~\LeftRightArrow~$ '.join(v for v in segments if v)

renderer = {
    r'\# of form': render_desc_other_forms,
}
default_renderer = lambda x: CROSS if x else EMPTY  # used if column not in renderer dict

lambda segs: ' ' + ' + '.join(segs) + ' '
print(r"""
\begin{table}
    \centering\footnotesize\tabcolsep=0.11cm
    \begin{tabular}{|c|c|c||c|c|c||c|c|c||c|c||c|}
    \cline{1-9}
    \multicolumn{9}{|c|}{Triplet composition (in node number)} & \multicolumn{3}{c}{} \\\hline
""")
print(r'\begin{tabular}{|' + '|'.join('c' for _ in columns) + '|}')
print(' ' + f' {COLSEP} '.join(columns) + r' \\\hline\hline')
for a, b, c in itertools.product(A_CASES, B_CASES, C_CASES):
    if is_canonical(a, b, c) or True:
        line = COLSEP.join((
            str(renderer.get(col, default_renderer)(call(a, b, c))).center(len(col)+2)
            for col, call in columns.items()
        ))
        print(line + r'\\\hline')
print(r"""
    \end{tabular}
    \caption{Canonicity and number of alternative writing of all triplets according to their node composition. The rightmost column indicates the number of alternative writing, based on the number of node in set $C$, and on the permutation of sets $A$ and $B$, noted $A\leftrightharpoons B$.}
    % see ~/packages/powergrasp/triplet/combinations.py for generation of that table (it has been edited directly here since)
    \label{tab:triplet-concept:canonicity-distribution}
\end{table}   % Table tab:triplet-concept:canonicity-distribution
""")
