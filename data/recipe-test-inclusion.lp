% A test of recipe behavior, where an existing powernode
%  must be reused inside a new one.

edge((a;b),(c;d;e;f)).
edge((e;f),(g;h)).

% With a recipe forcing ef×gh to be compressed first,
%  we should get a ab×cd(ef) motif on second step.
