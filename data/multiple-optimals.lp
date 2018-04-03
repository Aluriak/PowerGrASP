% Multiple bicliques of same score, to test multishot motif search.

edge((a1;b1),(c1;d1;e1)).
edge((a2;b2),(c2;d2;e2)).
edge((a3;b3),(c3;d3;e3)).

% Make them in the same cc
edge(a,(a1;a2;a3)).

% Show that further compression is not impacted.
edge((a;b),(f1;f2)).

