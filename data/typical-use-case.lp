% The typical use case for the lattice-based search space formalization.

edge((a;b;c),(e;d)).
edge(g,e).
edge((d;i;j;k),(e;f;g;h)).

% motifs to compress (for ~/pocs/generalist_compression)
motif(1,e,(a;b;c;d;g;i;j;k)).  % concept 1
motif(2,g,(d;i;j;k)).          % concept 2
motif(3,(d;i;j;k),(f;g;h)).    % concept 3
motif(4,d,(a;b;c)).            % concept 7

