%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best biclique from preprocessed information on the non-covered graph
%
% initial version:  09/12/2014   J. Nicolas
% revised version:  29/04/2015   L. Bourneuf
% revised version:  08/07/2015   L. Bourneuf
% revised version:  26/03/2018   J. Nicolas
%
% Constants:
%       - cc: treated connected component. (cc/1 gives existing cc).
%       -  k: current step of treatment (first step is 1).
%       - upperbound: the maximal reachable cover.
%       - max_set_size: the maximal reachable size of a set.
% Input:
%       - inter(X,Y): there exist an edge linking X and Y in cc.
%       - edge(X,Y): there exist a edge linking X and Y in cc (X<Y).
%       - membercc(Y): Y is a member of cc.
% Output:
%       - newconcept(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - star(cc,k,T): set T of concept is a singleton.
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
1{minobj(cc,k,X): membercc(X)}1.

% Choice of elements in set 1
newconcept(cc,k,1,X):- minobj(cc,k,X).
0 { newconcept(cc,k,1,X): linked2(Min,X) } max_set_size :- minobj(cc,k,Min).

% Choice of elements in set 2, using nb_node if available
1 { newconcept(cc,k,2,Y): inter(Min,Y), Min<Y } max_set_size :- minobj(cc,k,Min).

% An element in a set can't be in the other set.
:- newconcept(cc,k,1,X) ; newconcept(cc,k,2,X).

% A node can't be in a set if not linked to a node of other set
:- newconcept(cc,k,1,X) ; newconcept(cc,k,2,Y) ; not inter(X,Y).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% a star is a biclique with one powernode composed of only one node
%%star(cc,k,T):- 1 { newconcept(cc,k,T,X): weight(X,1) } 1 ; T=1..2.
star(cc,k,T):- 1 { newconcept(cc,k,T,X) } 1 ; T=1..2.

%Do not accept single edges
:- star(cc,k,1) ; star(cc,k,2). 
