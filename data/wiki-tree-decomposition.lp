% Graph from wikipedia's tree decomposition page.
%  https://en.wikipedia.org/wiki/Tree_decomposition

edge(a,(b;c)).
edge(d,(c;e)).
edge(f,(b;g)).
edge(h,(e;g)).

edge(b,(c;e;g)).
edge(e,(c;b;g)).
