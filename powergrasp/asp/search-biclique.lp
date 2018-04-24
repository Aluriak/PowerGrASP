%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best biclique in input graph.
%  A biclique here can't be a star, so there is at least two elements in each set.
%
% initial version:  09/12/2014   J. Nicolas
% revised version:  29/04/2015   L. Bourneuf
% revised version:  08/07/2015   L. Bourneuf
% revised version:  26/03/2018   J. Nicolas
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
%       - biclique: motif is a biclique
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% CONCEPTS %%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Symetric edges.
inter(X,Y):- edge(X,Y).
inter(X,Y):- inter(Y,X).

% X and Y share a neighbor.
linked2(X,Y):- inter(X,Z) ; inter(Y,Z) ; X<Y.

% Choice of the minimum of the concept
1{minobj(X): inter(X,_)}1.

% Choice of elements in set 1
newconcept(1,X):- minobj(X).
1 { newconcept(1,X): linked2(Min,X) } max_set_size :- minobj(Min).

% Choice of elements in set 2, using nb_node if available
2 { newconcept(2,Y): inter(Min,Y), Min<Y } max_set_size :- minobj(Min).

% An element in a set can't be in the other set.
:- newconcept(1,X) ; newconcept(2,X).

% A node can't be in a set if not linked to a node of other set
:- newconcept(1,X) ; newconcept(2,Y) ; not inter(X,Y).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

biclique.
