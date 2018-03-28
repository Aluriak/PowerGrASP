%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform post-processing of the data at each steps.
%  its not a standalone program, but a set of rules that needs to be grounded with
%  programs find best clique and find best biclique program
%  the post processing consist of rules shared by cliques and bicliques,
%  like parent block or include block rules, and the associated constraints.
%
%  more important : postprocessing is based on atoms newconcept, clique and star
%  produced (or not) by findbestbiclique and findbestclique.
%  The maximal lowerbound optimization of concept score is performed by postprocessing.
%
% initial version:  09/07/2014   L. Bourneuf
% revised version:  26/03/2018   J. Nicolas
%
% Constants:
%       -  k: current step of treatment (first step is 1)
%       - lowerbound: the minimal score (see 'lowerbound optimization')
%       - upperbound: the maximal score (see 'lowerbound optimization')
%
% Input (from findbestclique or findbestbiclique):
%       - newconcept(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - clique(cc,k): concept is a clique.
%       - star(cc,k,T): set T of concept is a star.
% Input (common data):
% Output:
%       - powernode(cc,k,T,X): X is the member of the set T in the concept cc at step k.
%       - poweredge(cc,K1,T1,K2,T2): powernode K1,T1 is linked to powernode K2,T2.
%       - poweredge(cc,K1,T1,X): powernode K1,T1 is linked to node X.
%       - covered(X,Y): oriented edge X to Y is covered by concept.
%       - include_block(k,B,p(cc,k,T)): block B contains set T of newconcept.
%       - block(k,B,X): block B contains X.
%       - include_powernode(cc,K1,T1,K2,T2): powernode K1,T1 contains K2,T2.
%       - powernode_count(S): S new powernodes are generated.
%       - score(S): concept cc at step k is a motif of score S.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% clique: create an edge to powernode itself / don't need to create two powernodes
poweredge(p(cc,k,1),p(cc,k,1)):- clique(cc,k).
% star: link directly the singleton set to the second powernode
poweredge(p(cc,k,3-T),      X):- star(cc,k,T) ; newconcept(cc,k,T,X).
% in all other cases: create a poweredge between the two newconcepts
poweredge(p(cc,k,1),p(cc,k,2)):- not clique(cc,k) ; not star(cc,k,T): T=1..2.

poweredge_count(1).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%  BLOCKS  %%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% A block created at step k-1 intersects  the set T of the newconcept if they share at least one element
block_intersects_newconcept(k,p(cc,L,U),T):- block(k-1,p(cc,L,U),X) ; newconcept(cc,k,T,X).
block_intersects_newconcept(k,cc,T):- block(k-1,cc,X) ; newconcept(cc,k,T,X).

% Newconcept T fits perfectly powernode cc,L,U, so no new power node has to be generated
perfectfit(T,p(cc,L,U)):-  block_intersects_newconcept(k,p(cc,L,U),T); L<k; not star(cc,k,T);
                            block(k-1,p(cc,L,U),X):  newconcept(cc,k,T,X);
                            newconcept(cc,k,T,Y): block(k-1,p(cc,L,U),Y).
is_perfectfit(cc,k,T):- perfectfit(T,_).

%Management of blocks at step k
% nodes covered by a powernode are set in the associated block
block(k,p(cc,k,1),X):- newconcept(cc,k,1,X) ; not star(cc,k,1).
block(k,p(cc,k,2),X):- newconcept(cc,k,2,X) ; not star(cc,k,2) ; not clique(cc,k).

% keep nodes not covered by new concept in their block
block(k,P,X):- membercc(X) ; not newconcept(cc,k,T,X): T=1..2 ; block(k-1,P,X).
block(k,P,X):- newconcept(cc,k,T,X) ; star(cc,k,T) ; block(k-1,P,X) ; T=1..2.

% B is a parent block of P if it contains it and no other block contained in B contains P.
parent_block(B,T):- block_intersects_newconcept(k,B,T) ;
                    not {include_block(k-1,B,Z) ; block_intersects_newconcept(k,Z,T)}.

                    
% Block inclusion : keep trace of block hierarchy
%  algorithmic for the block P of the new concept, and its parent_block B:
%    if all nodes of B are in P (<=> P == B): done
%    else: (<=> P is included in B)
%      create include_block(k,B,P)
%      for each block C in B:
%        assert(C is included in P OR C inter P = {0})
%        if C included in P:
%          don't create include_block(k,B,C)
%          create include_block(k,P,C)
%        else: (C inter P = {0})
%          do nothing else
%
%  in a more logical way:
%    - P is included in B
include_block(k,B,p(cc,k,1)):- parent_block(B,1).
include_block(k,B,p(cc,k,2)):- parent_block(B,2) ; not clique(cc,k).
%    - all blocks included in B that are in P are included in P instead of B
include_block(k,p(cc,k,T),C):- parent_block(B,T) ; C=p(cc,L,U) ; block(k-1,C,E); L<k  ;
                            newconcept(cc,k,T,E) ;
                            include_block(k-1,B,C).
%    - all blocks that aren't in P are kept "as is" for next step
include_block(k,B,C):- C=p(cc,L,U) ; block(k-1,C,_); L<k  ;
                       0{block(k-1,C,E): newconcept(cc,k,T,E)}0;
                       %  not block_intersects_newconcept(k,C,_);
                       not include_block(k,p(cc,k,T),C):T=1..2;
                       include_block(k-1,B,C).





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% RESULTS %%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

special_node(1):- clique(cc,k).
special_node(T):- star(cc,k,T); T=1..2.
special_node(T):- is_perfectfit(cc,k,T).

powernode_count(0):- special_node(1); special_node(2).
powernode_count(1):- special_node(T); not special_node(3-T); T=1..2.
powernode_count(2):- not special_node(1); not special_node(2).

#show.

% powernodes and poweredge
#show powernode(cc,k,T,X): newconcept(cc,k,T,X) ; not clique(cc,k) ; not star(cc,k,T).
#show powernode(cc,k,1,X): newconcept(cc,k,_,X) ;     clique(cc,k).
#show poweredge(cc,K1,T1,K2,T2): poweredge(p(cc,K1,T1),p(cc,K2,T2)).
#show poweredge(cc,K1,T1,X): poweredge(p(cc,K1,T1),X) , newconcept(cc,k,_,X).
#show star(X): star(cc,k,T) ; newconcept(cc,k,T,X).

% data about new partition
#show block(k,P,X): block(k,P,X).  % output only new blocks.
#show include_block(k,B,C): include_block(k,B,C).

% statistics
#show powernode_count/1.
#show poweredge_count/1.
%%#show powernode_count(2-P): not clique(cc,k) , not star(cc,k,1), not star(cc,k,2), P={perfectfit(_,_)}.
%%#show poweredge_count(K): K={poweredge(_,_)}.
#show score/1.  % Warning, Python will use this and consider that the edge cover is the score.

% debug output
%#show clique/2.
%#show star/3.
%#show upper(upperbound).
%#show lower(lowerbound).
