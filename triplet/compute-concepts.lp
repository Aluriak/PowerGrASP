edge(X,Y) :- edge(Y,X).  % add symmetry
edge(X,X) :- edge(X,_).  % add reflexivity
ext(X) :- edge(X,_) ; edge(X,Y): int(Y).
int(Y) :- edge(_,Y) ; edge(X,Y): ext(X).
#show ext/1.
#show int/1.
