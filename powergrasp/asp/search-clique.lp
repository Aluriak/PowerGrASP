%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Find best clique from preprocessed information on the non-covered graph
%
% initial version:  09/12/2014   J. Nicolas
% revised version:  07/07/2015   L. Bourneuf
%
% Constants:
%       - cc: treated connected component. (cc/1 gives existing cc)
%       -  k: current step of treatment (first step is 1)
%
% Input:
%       - edge(X,Y): there exist an edge linking X and Y in cc. (X<Y)
% Output:
%       - newconcept(1,X): X is the member of the clique cc at step k.
%       - clique: motif is a clique.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% CONCEPTS %%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Symetric edges.
inter(X,Y):- edge(X,Y).
inter(X,Y):- inter(Y,X).

% Clique of 3 elements
clique3:- inter(X,Y); inter(Y,Z); inter(X,Z).

% Choice of a  clique of at least 3 elements
3 {newconcept(1,X): inter(X,_)}:- clique3.

% Consistency of the clique
:- newconcept(1,X); newconcept(1,Y) ; X<Y ; not inter(X,Y).

% Maximality of the clique
% :- clique3 ; membercc(X) ; not newconcept(1,X) ; inter(X,Y): newconcept(1,Y).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% CONCEPT PROPERTIES %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The found motif is a clique.
clique.
