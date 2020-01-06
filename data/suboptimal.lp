% Case proving that optimal compression can't always
%  be reached with standard heurisitic.

edge((a;b),(c;d;i;e;f)).
edge((c;d),(l;g;h)).
edge((e;f),(j;g;h)).
edge((g;h),(k;c;d)).


rel(X,Y):- rel(Y,X).
