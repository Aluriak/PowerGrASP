%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform scoring of the processed motif.
%  The score equals to the edge cover of the concept.
%
% initial version:  09/07/2014   L. Bourneuf
% revised version:  26/03/2018   J. Nicolas
% revised version:  27/03/2018   L. Bourneuf
%
% Constants:
%       - k: current step of treatment (first step is 1)
%       - lowerbound: the minimal score
%       - upperbound: the maximal score
%
% Input (from findbestclique or findbestbiclique and postprocessing):
%       - newconcept(T,X): X is the member of the set T in the concept cc at step k.
%       - clique: concept is a clique.
%       - biclique: motif is a biclique.
%       - star(T): motif is a biclique and a star, with set T as the hub.
% Output:
%       - score(S): motif has score S.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%% EDGE COVER %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Edge cover is computed as the number of edges replaced by the poweredge.
%  the score is defined as the upperbound (maximal edge cover) minus edge cover.
%  bigger is the edge cover, smaller is the score.
%  solver's job is to minimize the score, thus maximize the edge cover.

% Node count in each set of the biclique is given by summing weights of all nodes.
% Edge cover is the number of node covered by the set.
edgecover(T,N):- biclique ; T=1..2 ; N={newconcept(T,X)}.
edgecover(1,N):- clique   ; N={newconcept(1,X)}.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% SCORE OPTIMIZATION %%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Concept score, equal to maximal score - edge cover.
score(N):- N=((N1*(N1-1))/2) ; N<=upperbound ; N>=lowerbound ; clique ; edgecover(1,N1).
score(N):- N<=upperbound; N>=lowerbound; star(T) ; edgecover(3-T,N).
score(N):- N=N1*N2; N<=upperbound; N>=lowerbound; biclique ; not star(1); not star(2);
           edgecover(1,N1) ; edgecover(2,N2).

% Minimize score
#minimize{(upperbound-S)@1,S:score(S)}.

% Discard cases when no score is generated
:- not score(_).
#show score/1.  % Warning, Python will use this and consider that the edge cover is the score.
