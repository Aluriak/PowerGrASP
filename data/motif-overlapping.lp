% Show examples of motif overlapping.

% A biclique is compressed, revealing a clique of three elements.
edge((a;b;c),(d;e;f)).
edge((a;b;c),(a;b;c)).

% Two cliques are shallowed by a star.
edge((a1;a2;a3;a4;a5),(a1;a2;a3;a4;a5)).  % first clique
edge((b1;b2;b3;b4),(b1;b2;b3;b4)).  % smaller clique
edge(h,(a1;b4)).  % hub
edge(h,(c1;c2;c3;c4;c5;c6;c7;c8;c9)).  % enough nodes to make the star the biggest motif

% A clique is eaten by a biclique.
edge((x1;x2;x3;x4),(x1;x2;x3;x4)).  % the clique
edge((x4;y1;y2),(z1;z2;z3)).  % 3×3 biclique.
