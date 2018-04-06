% Show that a powernode must include all nodes in the powernodes he contains.
%  In opposition to inclusions.lp, this case shows when the powernode can't be created.
%  The final star motif a×bd can't be created because b and d are in different blocks.
%  However, until this test case, a powernode was created, with all nodes of the score 8
%   motif inside, linked to a, leading falsely to the observation that a was linked
%   to all nodes.
%  This was only detected because in some case such inconsistency is rendered
%   very poorly in cytoscape.

% If this test case must fail, probably there is no enforcement of the following rule:
%  if a powernode P includes a node in a block B and a node outside B,
%  then all nodes in B must be in P.

% All nodes are in a ubiquitous powernode.
edge((root;root2;root3),(a;b;c;d;e;f;g;h;i;j;l;m)).  % score 36

% A motif is built inside the ubiquitous powernode.
edge((b;c),(d;e;f;g;h)).  % score 8

% The star creating (theoretically) the powernode including the motif.
edge(a,(b;d)).  % score 6: note the absence of e, f, g and h
