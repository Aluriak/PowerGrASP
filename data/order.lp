% This use case is about node ordering in the graph.
% In ASP, nodes are ordered lexicographically,
%  but integers are always smaller than litterals,
%  that are always smaller than string.

edge(10,4).
edge(10,5).
edge(10,6).

edge(a,10).
edge("a",a).
