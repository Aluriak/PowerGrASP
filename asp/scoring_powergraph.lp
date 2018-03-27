%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform scoring of the postprocessed data at each steps.
%  The score equals to the edge cover of the concept.
%
% The scoring consists of rules allowing the generation of score(N),
%  providing the score of the produced concept.
%  its not a stand alone program, but a set of rules that needs to be grounded with
%  findbestmotif and postprocessing programs
%
% initial version:  09/07/2014   L. Bourneuf
% revised version:  26/03/2018   J. Nicolas
%
% Constants:
%       - cc: treated connected component. (cc/1 gives existing cc)
%       -  k: current step of treatment (first step is 1)
%       - lowerbound: the minimal score
%       - upperbound: the maximal score
%
% Input (from findbestclique or findbestbiclique and postprocessing):
%       - newconcept(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - clique(cc,k): concept is a clique.
%       - star(cc,k,T): set T of concept is the singleton of a star.
% Output:
%       - score(S): concept cc at step k is a motif of score S.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Are covered all edges of concept that link two nodes of different sets.
covered(cc,k,X,Y):- newconcept(cc,k,T,X) ; newconcept(cc,k,3-T,Y) ; X<=Y ; T=1..2.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%% EDGE COVER %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Edge cover is computed as the number of edges replaced by the poweredge.
%  the score is defined as the upperbound (maximal edge cover) minus edge cover.
%  bigger is the edge cover, smaller is the score.
%  solver's job is to minimize the score, thus maximize the edge cover.

% Node count in each set of the biclique is given by summing weights of all nodes.
% Edge cover is the number of node covered by the set.
edgecover(cc,k,T,N):- T=1..2 ; not clique(cc,k); N={newconcept(cc,k,T,X)}.
edgecover(cc,k,1,N):-  clique(cc,k); N={newconcept(cc,k,1,X)}.
%edgecover(cc,k,T,N):- newconcept(cc,k,T,_) ; N=#sum{W,X:weight(X,W), newconcept(cc,k,T,X)}.

% Concept score, equal to maximal score - edge cover.
score(N):- N<=upperbound; N>=lowerbound; star(cc,k,T); edgecover(cc,k,3-T,N).
score(N):- N=((N1*(N1-1))/2); N<=upperbound; N>=lowerbound; clique(cc,k);
           edgecover(cc,k,1,N1).
score(N):- N=N1*N2; N<=upperbound; N>=lowerbound; not clique(cc,k); not star(cc,k,1); not star(cc,k,2);
           edgecover(cc,k,1,N1) ; edgecover(cc,k,2,N2).
%score(N):- N=upperbound-(N1*N2); N>=0   ; not clique(cc,k)    ;
%           edgecover(cc,k,1,N1) ; edgecover(cc,k,2,N2).
%score(N):- N=upperbound-((N1*(N1-1))/2) ; N>=0 ; clique(cc,k) ;
%           edgecover(cc,k,1,N1).
%score(N):- N=upperbound-((N1*(N1-1))/2) ; N>=0 ; clique(cc,k) ;
%           N1={newconcept(cc,k,1,X)}.

% Minimize score
%%#minimize{S@1,S:score(S)}.
#minimize{(upperbound-S)@1,S:score(S)}.

% Exclusion of concepts with not enough nodes.
%  The lowerbound is equals to 1 at least,
%  and determined by the scorebound ASP program.
%  The upperbound is the min between the number of remaining edges
%  in the connected component and the size of the previous concept.
%%:- score(S) ; S>upperbound-lowerbound.

% Discard cases when no score is generated
:- not score(_).
