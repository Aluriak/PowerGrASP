%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extraction of graph data from edge information.
%
% initial version:  09/12/2014   J. Nicolas
% revised version:  29/04/2014   L. Bourneuf
%
% Extract the connected components of the graph
% Input:
%       - edge(X,Y): there exists an edge between X and Y in the graph.
% Output (one model per connected component):
%       - cc(CC): CC is the minimal element of a connected component.
%       - membercc(X,Y): there exists a path from X to Y, X<Y.
%       - edge(X,Y): there exists an edge between X and Y.
%       - block(0,CC,X): X is in the block cc a step 0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% CONNECTED COMPONENTS SEARCH %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Symetric graph
inter(X,Y):- edge(X,Y) ; X!=Y.
inter(X,Y):- inter(Y,X).

% Node access.
node(X):- inter(X,_).

% An Oriented edge go from smaller to bigger :
% oedge(3, 5) is true, oedge(5, 3) is false.
oedge(X,Y):- edge(X,Y) ; X<Y.
oedge(X,Y):- edge(Y,X) ; X<Y.

% Connected paths starting with minimal element X
% connected(Minimum element,Element connected to the minimum)
connectedpath(X,Y):- oedge(X,Y).
connectedpath(X,Z):- connectedpath(X,Y) ; inter(Y,Z) ; X<Z.

% Connected components are identified by their smaller element.
% Choose them, on by one.
1{ cc(X): node(X) , not connectedpath(_,X) }1.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%% CONNECTED COMPONENTS YIELDING %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Are members of the cc all nodes linked to the smaller element, this last included.
membercc(X):- cc(CC) ; node(X) ; connectedpath(CC,X).
membercc(CC):- cc(CC).

% initial ccstate of blocks : each node is in its cc
block(0,CC,X):- membercc(X) ; cc(CC).

% outputs
#show cc/1.
#show membercc/1.
#show block/3.
#show edge(X,Y): oedge(X,Y), membercc(X).
#show nb_cc(N): N={node(X): node(X), not connectedpath(_,X)}.
