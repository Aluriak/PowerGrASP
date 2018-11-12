%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best star in input graph.
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
%       - star(T): motif is a star, set T is the hub.
%       - biclique: motif is a biclique.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% CONCEPTS %%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Symetric edges.
inter(X,Y):- edge(X,Y).
inter(X,Y):- inter(Y,X).

% Choice of the hub.
1{newconcept(2,Hub): inter(Hub,_)}1.

% Choice of at least 2 elements in set 1.
min_size(2):- lowerbound<2.
min_size(lowerbound):- lowerbound>=2.
MS { newconcept(1,Y): inter(Hub,Y) } upperbound :- newconcept(2,Hub) ; min_size(MS).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A star is a biclique with one powernode composed of only one node.
star(2).

biclique.
