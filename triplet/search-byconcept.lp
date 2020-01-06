% Search for a maximal triplet, using concept method.
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
% cover(N) :- N=(Na*Nb)+(Na*Nc)+(Nb*Nc)+(Nc*(Nc-1))/2 ; Na = {a(_)} ;  Nb = {b(_)} ;  Nc = {c(_)}.

% #maximize{N:cover(N)}.
#show a/1.
#show b/1.
#show c/1.


#const min_a=0.
#const min_b=0.
#const min_c=0.
#const max_a=#sup.
#const max_b=#sup.
#const max_c=#sup.

:- {a(_)}min_a-1.
:- {b(_)}min_b-1.
:- {c(_)}min_c-1.
:- max_a+1{a(_)}.
:- max_b+1{b(_)}.
:- max_c+1{c(_)}.


% Mining of triplet concepts, by deriving a triplet from each formal concept
%  found in the graph context with all reflexive edges.
%  Don't care positions to yield triplet concepts seems to not be necessary.


% Ensure symmetry of the input relation.
rel(X,Y) :- rel(Y,X).
rel(X,X) :- rel(X,_).  % use all reflexive edges

% Mine formal concepts.
obj(O) :- rel(O,_) ; rel(O,A): att(A).
att(A) :- rel(A,_) ; rel(O,A): obj(O).

% Convert formal concept as triplet.
a(O) :- obj(O) ; not att(O).
b(A) :- att(A) ; not obj(A).
c(C) :- obj(C) ; att(C).

% break symmetry
:- b(A) ; A<O: a(O).

% Ignore infimum and supremum when empty.
:- not a(_) ; not c(_).
:- not b(_) ; not c(_).

% When B is empty, the complementary graph of A
%  shouldn't have 2 or more connected components.
same_cc(M) :- M=#min{X:a(X)}.
same_cc(X) :- a(X) ; not rel(X,Y) ; same_cc(Y).
:- a(X) ; not same_cc(X) ; not b(_).

% if B is empty, no element outside A union C
% is related both to all but one element of C and to all elements of A
% :- not b(_) ; not a(X) ; not c(X) ; rel(X,_) ; c(K) ; rel(X,Y): a(Y) ; rel(X,Z): c(Z), Z!=K.
% Admissibility conditions:
%  If there is an outsider element linked to A U B U C, the concept is not admissible.
abc(X) :- a(X).  abc(Y) :- b(Y).  abc(C) :- c(C).
outsider(X) :- rel(X,_) ; not abc(X).
:- abc(_) ; outsider(Y) ; rel(X,Y): abc(X).
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
