% this is a case where the prioritization by node degree show its effect.

% biclique that is normally the first motif to be compressed: {a,b,c}×{d,e}
edge((a;b;c),(d;e)).

% star with central node as the node with the maximal degree, overlapping the biclique.
%  will be compressed first if prioritization by degree is used.
edge(s,(a;f;g;h)).  % a is linked to 5 over nodes.
