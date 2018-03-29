% first biclique
edge((a;d;d2),(b1;b2;c;e;q;o)).
edge(b1,c).

% second biclique
edge((i;h),(f1;f2;g;j;l;p)).
edge(f1,g).

% m and n are linked to l,p,q and o
edge((m;m2;n),(l;p;q)).

% m, m2 and n is a clique
edge(n,(m;m2)).
