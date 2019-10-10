%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best mu-quasibiclique in input graph.
%
% Constants:
%       - k: current step of treatment (first step is 1).
%       - lowerbound: the minimal cover to reach.
%       - upperbound: the maximal reachable cover.
%       - max_set_size: the maximal reachable size of a set.
%       - mu: the mu value for quasibiclique constraints.
% Input:
%       - edge(X,Y): there exist a edge linking X and Y in cc (X<Y).
% Output:
%       - newconcept(T,X): X is a member of the set T of currently processed motif.
%       - quasibiclique: motif is a quasibiclique
%       - biclique: motif is a biclique
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#const mu=2.

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

% Choice of elements in set 2
2 { newconcept(2,Y): edge(_,Y) } max_set_size :- minobj(Min).

% An element in a set can't be in the other set.
:- newconcept(1,X) ; newconcept(2,X).

% DEBUG
% minobj("r").
% newconcept(1,("s";"t";"r";"v";"u")).
% % newconcept(1,"u").
% newconcept(2,("p";"q";"x";"y";"z")).
% % newconcept(2,"z").
% #show newconcept/2.

% Nodes not linked to another of the motif.
unlinked(X,Y) :- newconcept(1,X) ; newconcept(2,Y) ; not inter(X,Y).
unlinked(Y,X) :- unlinked(X,Y).
% A node is disconnected to at most mu number of vertices in the other set.
:- newconcept(_,X) ; mu+1 { unlinked(X,_) }.
% A node is adjacent to at least mu number of vertices in the other set.
:- newconcept(T,X) ; { inter(X,Y): newconcept(3-T,Y) } mu-1.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% A star is a biclique with one powernode composed of only one node
star(T):- 1 { newconcept(T,X) } 1 ; T=1..2.

% Do not accept single edges
:- star(1) ; star(2).

biclique.
quasibiclique.
