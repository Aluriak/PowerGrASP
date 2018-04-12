%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Perform processing of the motif discovered by another program.
%  its not a standalone program, but a set of rules
%  that needs to be grounded with programs `search-*.lp`.
%  the processing consist of general rules shared by cliques and bicliques,
%  like parent block or include block rules, and the associated constraints.

% A constraint for block overlap avoidance should be grounded with that program.
%
% initial version:  09/07/2014   L. Bourneuf
% revised version:  26/03/2018   J. Nicolas
% revised version:  27/03/2018   L. Bourneuf
%
% Constants:
%       - k: current step of treatment (first step is 1)
%       - lowerbound: the minimal score (see 'lowerbound optimization')
%       - upperbound: the maximal score (see 'lowerbound optimization')
%       - covered_edges_from_asp: to make true if covered_edge/2 atoms must be yield
%
% Input (from findbestclique or findbestbiclique):
%       - newconcept(T,X): X is a member of the set T of currently processed motif.
%       - clique: motif is a clique.
%       - biclique: motif is a biclique.
%       - star(T): motif is a biclique and a star, with set T as the hub.
% Output:
%       - powernode(T,X): X is the member of the set T in the compressed motif.
%       - poweredge(K1,T1,K2,T2): powernode K1,T1 is linked to powernode K2,T2.
%       - poweredge(K1,T1,X): powernode K1,T1 is linked to node X.
%       - covered_edge(X,Y): edge X to Y is covered by motif (ONLY IF covered_edges_from_asp is true).
%       - powernode_count(S): S new powernodes are generated.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%  BLOCKS  %%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% A node is contained by all blocks above the block containing it.
block(K,T,X):- block(L,U,X) ; include_block(K,T,L,U).

% Blocks created at step k-1 containing the set T of the motif.
block_contains_newconcept(L,U,T):- block(L,U,X) ; newconcept(T,X) ; block(L,U,Y): newconcept(T,Y).

% Newconcept T fits perfectly powernode cc,L,U, so no new power node has to be generated
perfectfit(L,U,T):-  block_contains_newconcept(L,U,T) ; L<k ; not star(T) ;
                     newconcept(T,Y): block(L,U,Y).

% New concept may or may not be already present in the hierarchy.
powernode_integrated(L,U,X):- newconcept(T,X) ; perfectfit(L,U,T).
powernode_integrated(k,T,X):- newconcept(T,X) ; not perfectfit(_,_,T) ; not star(T).

% powernodes: those re-used, and those that didn't exist before.
#show powernode(K,T): biclique ; powernode_integrated(K,T,X) ; not star(U) ; newconcept(U,X).
#show powernode(K,T): clique   ; powernode_integrated(K,T,X).
#show new_powernode(T,X): biclique ; powernode_integrated(k,T,X) ; not star(U) ; newconcept(U,X).
#show new_powernode(1,X): clique   ; powernode_integrated(k,1,X).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%  HIERARCHY  %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% B is a parent block of P if it contains it and no other block contained in B contains P.
parent_block(KP,TP,T):- block_contains_newconcept(KP,TP,T) ; not perfectfit(KP,TP,T) ;
                        not include_block(KP,TP,KZ,TZ): block_contains_newconcept(KZ,TZ,T).


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
%    - powernode P is included in its parent block B
hierarchy_add(KP,TP,k,T):- parent_block(KP,TP,T) ; not star(T).
%    - all blocks included in B that are in P are included in P instead of B
change_hierarchy(KP,TP,k,T,L,U):-
    parent_block(KP,TP,T) ; % the parent block…
    include_block(KP,TP,L,U) ; L<k ;  % contains a block that is not the new one
    newconcept(T,E) ; block(L,U,E) ;  % so they share an element
    newconcept(T,E):  block(L,U,E).   % so other block is included in the new.
#show parent_block/3.

% Add the link between new powernode and the block it contains.
hierarchy_add(K1,T1,K2,T2):- change_hierarchy(_,_,K1,T1,K2,T2).
% Remove the link between the parent block and the block contained by powernode.
hierarchy_remove(K1,T1,K2,T2):- change_hierarchy(K1,T1,_,_,K2,T2).

% No overlap.
:- newconcept(T,E) ; block(L,U,E) ;  % an existing block and the new one share an element
   not block_contains_newconcept(L,U,T) ;  % but the block is not containing the new
   not change_hierarchy(_,_,k,T,L,U).  % nor is contained by the new.

#show hierarchy_add/4.
#show hierarchy_remove/4.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%  POWEREDGES  %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% clique: create an edge to powernode itself / don't need to create two powernodes
poweredge(1,1):- clique.
% star: link directly the singleton set to the second powernode
poweredge(3-T,X):- star(T) ; newconcept(T,X).
% in all other cases: create a poweredge between the two newconcepts
poweredge(1,2):- biclique ; not star(T): T=1..2.

% The poweredge will be drawn between integrated powernodes.
poweredge(K1,T1,K2,T2):- biclique ; not star(_) ; powernode_integrated(K1,T1,_) ; powernode_integrated(K2,T2,_) ; (K1,T1) < (K2,T2).
poweredge(K1,T1,S)    :- biclique ; star(T) ; newconcept(T,S) ; powernode_integrated(K1,T1,_).
poweredge(K1,T1,K1,T1):-   clique ; powernode_integrated(K1,T1,_).

#show poweredge/3.
#show poweredge/4.
#show poweredge_count(1).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%% OTHER OUTPUTS %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Count the number of new powernode
special_node(1):- clique.
special_node(T):- star(T); T=1..2.
special_node(T):- perfectfit(_,_,T).
powernode_count(0):- special_node(1); special_node(2).
powernode_count(1):- special_node(T); not special_node(3-T); T=1..2.
powernode_count(2):- not special_node(1); not special_node(2).
#show powernode_count/1.

% Are covered all edges of concept that link two nodes of different sets.
covered_edge(X,Y):- newconcept(T,X) ; newconcept(3-T,Y) ; X<Y ; T=1..2 ; biclique ; covered_edges_from_asp=1.
covered_edge(X,Y):- newconcept(1,X) ; newconcept(1,Y) ; X<Y ; clique ; covered_edges_from_asp=1.
#show covered_edge/2.

% A star is defined by the hub, not the set.
#show star(X): star(T) ; newconcept(T,X).

% Show only #showed atoms.
#show.
