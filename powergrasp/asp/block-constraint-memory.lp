% Implementation of the block overlap constraint, optimized for memory.
% If a powernode contains a node in a block and a node not in the block,
%  all nodes in block must be contained.
includedblock(L,U,T):- newconcept(T,X) ; block(L,U,X).  % X is in the block
strictlyincludedblock(L,U,T):-
    includedblock(L,U,T) ; newconcept(T,Z) ; not block(L,U,Z).  % Z is outside
:- strictlyincludedblock(L,U,T) ; not newconcept(T,Y) ; block(L,U,Y).  % Y is not in the pnode

% NB: this constraint may be written in many ways.
%  See debug/overlap-block-constraint for further investigations.
