%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best triplet concept in input graph.
%
% Constants:
%       - k: current step of treatment (first step is 1).
%       - lowerbound: the minimal cover to reach.
%       - upperbound: the maximal reachable cover.
%       - max_set_size: the maximal reachable size of a set.
% Input:
%       - edge(X,Y): there exist a edge linking X and Y in cc (X<Y).
% Output:
%       - newconcept(T,X): X is a member of the set T of currently processed motif.
%       - triplet: motif is a triplet
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% CONCEPTS %%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Symetric edges.
inter(X,Y):- edge(X,Y).
inter(X,Y):- inter(Y,X).

% Choice of elements in set 1
newconcept(1,X) :- a(X).
newconcept(2,X) :- b(X).
newconcept(3,X) :- c(X).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

star(T) :- newconcept(T,_) ; 1 { newconcept(T,_) } 1.
triplet_has_clique :- 2 { newconcept(3,_) }.
triplet.
#show a/1.
#show b/1.
#show c/1.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% TRIPLET MINING %%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Ensure reflexivity of the input relation.
inter(X,Y) :- inter(Y,X).

% % Choose the composition of triplet concepts.
{ a(O): inter(O,A) }.
{ b(A): inter(O,A) }.
{ c(C): inter(C,_) }.

% Ensure that sets are disjoint.
:- a(O) ; b(O).
:- c(O) ; b(O).
:- a(O) ; c(O).

% Ignore infimum and supremum when empty.
:- not a(_) ; not c(_).
:- not b(_) ; not c(_).


% Ensure existence of required rels between sets.
:- not inter(O,A) ; a(O) ; b(A).
:- not inter(O,C) ; a(O) ; c(C).
:- not inter(A,C) ; b(A) ; c(C).
:- not inter(D,C) ; c(D) ; c(C) ; C!=D.

% at least one edge in missing in sets A and B.
:- a(A) ; inter(A,B): a(B), B!=A.
:- b(A) ; inter(A,B): b(B), B!=A.

% if B is empty, no element outside A union C
% is related both to all but one element of C and to all elements of A
% :- not b(_) ; not a(X) ; not c(X) ; inter(X,_) ; c(K) ; inter(X,Y): a(Y) ; inter(X,Z): c(Z), Z!=K.
% Completely replaced by admissibility conditions !

% #show.
% #show a/1.
% #show int/1.
% #show cnd/1.

% maximality
% :- inter(P,_) ; not a(P) ; not c(P) ; inter(P,B): b(B) ; inter(P,C): c(C).
% :- inter(P,_) ; not b(P) ; not c(P) ; inter(P,A): a(A) ; inter(P,C): c(C).
% :- inter(P,_) ; not c(P) ; inter(P,A): a(A) ; inter(P,B): b(B) ; inter(P,C): c(C), P!=C.

% break symmetry
% :- b(A) ; A<O: a(O).

% Admissibility conditions:
% Prior definitions.
% outside(X) :- inter(X,_) ; not a(X) ; not b(X) ; not c(X).
% outside_to_a(X) :- outside(X) ; inter(X,Y): a(Y).
% outside_to_b(X) :- outside(X) ; inter(X,Y): b(Y).
% outside_to_c(X) :- outside(X) ; inter(X,Y): c(Y).
% outside_to_c_but_1(X) :- outside(X) ; 1{ not inter(X,C): c(C) }1.
% a_or_b_empty_set      :- not a(_).
% a_or_b_empty_set      :- not b(_).
% a_or_b_singleton      :- 1 { a(_) } 1.
% a_or_b_singleton      :- 1 { b(_) } 1.

% If an outsider element is linked to all but the elements of A or B,
%  the concept is not admissible.
% :- outside_to_a(X) ; outside_to_c(X).
% :- outside_to_b(X) ; outside_to_c(X).

% If A or B is emptyset or singleton, and an outsider element
%  linked to A U B U C but one of C, the concept is not admissible.
% :- a_or_b_empty_set ; outside_to_c_but_1(X)
   % ; outside_to_a(X) ; outside_to_b(X).
% :- a_or_b_singleton ; outside_to_c_but_1(X)
   % ; outside_to_a(X) ; outside_to_b(X).

% When B is empty, the complementary graph of A
%  shouldn't have 2 or more connected components.
% same_cc(M) :- M=#min{X:a(X)}.
% same_cc(X) :- a(X) ; not inter(X,Y) ; same_cc(Y).
% :- a(X) ; not same_cc(X) ; not b(_).
% singleton(b) :- 1 { b(_) } 1.
% :- a(X) ; not same_cc(X) ; singleton(b).

% At least one edge is missing in sets A and B.
% :- a(X) ; inter(X,Y): a(Y), X!=Y.
% :- b(X) ; inter(X,Y): b(Y), X!=Y.

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
