
% external clique
edge(a,b).
edge(a,c).
edge(a,d).
edge(a,e).
edge(b,c).
edge(b,d).
edge(b,e).
edge(c,d).
edge(c,e).
edge(d,e).

% external clique 2
edge((f;g;h;i;j;m),(f;g;h;i;j;m)).

% biclique of 4 elements of clique 1 and 2
edge(f,(a;b;c;d)).

% biclique of 4 elements of previous biclique and one external element
edge(l,f).
edge(l,g).
edge(l,h).
