


% Case study 1 for lattice-based compression
% edge(a,(b;c;d;x)).
% edge(b,(a;c;d;y)).
% edge(c,(a;b;z)).
% edge(d,(a;b;w)).


% Case study 2 for lattice-based compression: overlapping 3 and 4 cliques
% edge((a;b;c;d),(a;b;c;d)).  % first clique
% edge((d;e;f),(d;e;f)).  % small clique beside the first
% edge(b,g).  % noise


% Case study 3 for lattice-based compression: overlapping 4 cliques
% edge((a;b;d;e),(a;b;d;e)).  % first clique
% edge((b;c;e;f),(b;c;e;f)).  % second clique
% edge(b,g).  % noise


% Case study: suboptimal with some specifics removed
% suboptimal cutted-3 with some specifics removed
% edge((a;b),(c;d;g)).
% edge((c;d),(e;f;h)).
% edge((e;f),(a;b;i)).

% suboptimal cutted-4 with some specifics removed
% edge((a;b),(c;d;j)).
% edge((c;d),(e;f;k)).
% edge((e;f),(g;h;l)).
% edge((g;h),(a;b;i)).

% suboptimal cutted-5 with some specifics removed
% edge((a;b),(c;d;l)).
% edge((c;d),(e;f;m)).
% edge((e;f),(g;h;n)).
% edge((g;h),(i;j;o)).
% edge((i;j),(a;b;k)).

% suboptimal cutted-6 with some specifics removed
% edge((a;b),(c;d;n)).
% edge((c;d),(e;f)).
% edge((e;f),(g;h)).
% edge((g;h),(i;j;q)).
% edge((i;j),(k;l)).
% edge((k;l),(a;b)).
