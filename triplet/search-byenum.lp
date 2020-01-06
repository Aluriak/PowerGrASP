% Search for a maximal triplet.
% input:  edge(X,Y): X is linked to Y
rel(X,Y) :- edge(X,Y).

% Maximization:
% nb(a,Na) :- Na = {a(_)}.
% nb(b,Nb) :- Nb = {b(_)}.
% nb(c,Nc) :- Nc = {c(_)}.
% cover(ab,N) :- N=Na*Nb ; nb(a,Na) ; nb(b,Nb).
% cover(ac,N) :- N=Na*Nc ; nb(a,Na) ; nb(c,Nc).
% cover(bc,N) :- N=Nb*Nc ; nb(b,Nb) ; nb(c,Nc).
% cover(cc,N) :- N=(Nc*(Nc-1))/2 ; nb(c,Nc).
% cover(N) :- N=#sum{X:cover(_,X)}.
% One-liner (much more quicker to ground):
% cover(N) :- N=(Na*Nb)+(Na*Nc)+(Nb*Nc)+(Nc*(Nc-1))/2 ; Na = {a(_)} ;  Nb = {b(_)} ;  Nc = {c(_)}.
% cover(Na+Nb+Nc) :- Na = {a(_)} ;  Nb = {b(_)} ;  Nc = {c(_)}.

% #maximize{N:cover(N)}.
% #show cover/1.
#show a/1.
#show b/1.
#show c/1.


#const min_a=0.
#const min_b=0.
#const min_c=0.
#const max_a=#sup.
#const max_b=#sup.
#const max_c=#sup.



% Ensure symmetry of the input relation.
rel(X,Y) :- rel(Y,X).

% Choose the composition of triplet concepts.
min_a { a(O): rel(O,A) } max_a.
min_b { b(A): rel(O,A), a(O), not a(A) } max_b.
min_c { c(C): rel(C,_), not a(C), not b(C) } max_c.
% 1 { a(O): rel(O,A) }.
% 1 { b(A): rel(O,A) }.
% 3 { c(C): rel(C,_) }.
% :- a(O) ; b(O).
% :- a(O) ; c(O).
% :- b(O) ; c(O).

% 1{triangle(X,Y,Z)}1:- rel(X,Y) ; rel(Y,Z) ; rel(Z,X) ; X<Y ; Y<Z.
% c(X):- triangle(X,_,_).
% c(X):- triangle(_,X,_).
% c(X):- triangle(_,_,X).

% Alternative generation.
% neighbors(X) :- rel(X,_) ; not a(X) ; not b(X) ; rel(X,O): a(O) ; rel(X,A): b(O).
% { c(C): neighbors(C) }.

% Ensure that sets are disjoint.
% :- a(O) ; b(O).
% :- c(O) ; b(O).
% :- a(O) ; c(O).

% Ignore infimum and supremum when empty.
:- not a(_) ; not c(_).
:- not b(_) ; not c(_).


% Ensure existence of required rels between sets.
:- not rel(O,A) ; a(O) ; b(A).
:- not rel(O,C) ; a(O) ; c(C).
:- not rel(A,C) ; b(A) ; c(C).
:- not rel(D,C) ; c(D) ; c(C) ; C!=D.

% at least one edge in missing in sets A and B.
:- a(A) ; rel(A,B): a(B), B!=A.
:- b(A) ; rel(A,B): b(B), B!=A.

% When B is empty, the complementary graph of A
%  shouldn't have 2 or more connected components.
same_cc(M) :- M=#min{X:a(X)}.
same_cc(X) :- a(X) ; not rel(X,Y) ; same_cc(Y).
:- a(X) ; not same_cc(X) ; not b(_).

% if B is empty, no element outside A union C
% is related both to all but one element of C and to all elements of A
% :- not b(_) ; not a(X) ; not c(X) ; rel(X,_) ; c(K) ; rel(X,Y): a(Y) ; rel(X,Z): c(Z), Z!=K.
% Completely replaced by admissibility conditions !

% #show.
% #show a/1.
% #show int/1.
% #show cnd/1.

% maximality
% :- rel(P,_) ; not a(P) ; not c(P) ; rel(P,B): b(B) ; rel(P,C): c(C).
% :- rel(P,_) ; not b(P) ; not c(P) ; rel(P,A): a(A) ; rel(P,C): c(C).
% :- rel(P,_) ; not c(P) ; rel(P,A): a(A) ; rel(P,B): b(B) ; rel(P,C): c(C), P!=C.

% break symmetry
:- b(A) ; A<O: a(O).

% Admissibility conditions:
%  If there is an outsider element linked to A U B U C, the concept is not admissible.
abc(X) :- a(X).  abc(Y) :- b(Y).  abc(C) :- c(C).
outsider(X) :- rel(X,_) ; not abc(X).
% :- abc(_) ; outsider(Y) ; rel(X,Y): abc(X).
%  If an outsider element is linked to all but the element of A or B, the concept is not admissible.
:- node_linked_to_a(X) ; node_linked_to_clique(X).
:- node_linked_to_b(X) ; node_linked_to_clique(X).
%  If A or B is emptyset or singleton, and an outsider element linked to A U B U C but one of C, the concept is not admissible.
a_or_b_empty_set :- not a(_).
a_or_b_empty_set :- not b(_).
a_or_b_singleton :- 1 { a(_) } 1.
a_or_b_singleton :- 1 { b(_) } 1.
unrel_to_clique(X,C) :- outsider(X) ; c(C) ; not rel(X,C).
node_linked_to_all_but_one_c(X) :- 1 { unrel_to_clique(X,_) } 1 ; outsider(X).
:- a_or_b_empty_set ; node_linked_to_all_but_one_c(X) ; node_linked_to_a(X) ; node_linked_to_b(X).

node_linked_to_a(X) :- outsider(X) ; rel(X,Y): a(Y).
node_linked_to_b(X) :- outsider(X) ; rel(X,Y): b(Y).
node_linked_to_clique(X) :- outsider(X) ; rel(X,Y): c(Y).
:- a_or_b_singleton ; node_linked_to_all_but_one_c(X) ; node_linked_to_a(X) ; node_linked_to_b(X).

% cover computation
% size_c(Z) :- Z={c(_)}.
% size_a(Z) :- Z={a(_)}.
% size_b(Z) :- Z={b(_)}.
% cover(SC*SA + SC*SB + SA*SB + (SC*(SC-1))/2) :- size_c(SC) ; size_a(SA) ; size_b(SB).
% cover_ab(SA*SB) :- size_c(SC) ; size_a(SA) ; size_b(SB).
% cover_cc((SC*(SC-1))/2) :- size_c(SC) ; size_a(SA) ; size_b(SB).
% cover_bc(SC*SB) :- size_c(SC) ; size_a(SA) ; size_b(SB).
% cover_ac(SC*SA) :- size_c(SC) ; size_a(SA) ; size_b(SB).
% :- cover(0).
