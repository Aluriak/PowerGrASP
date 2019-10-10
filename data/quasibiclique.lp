% This networks is made of multiple 2-balanced biclique.


edge(a,f).                          edge(a,i).  edge(a,j).  % minobj is not linked to everyone
edge(b,f).  edge(b,g).  edge(b,h).  edge(b,i).  edge(b,j).
edge(c,f).  edge(c,g).  edge(c,h).  edge(c,i).  edge(c,j).
edge(d,f).  edge(d,g).  edge(d,h).              edge(d,j).
edge(e,f).  edge(e,g).  edge(e,h).  edge(e,i).  edge(e,j).


edge(r,q).  edge(r,x).  edge(r,y).  edge(r,z).  edge(r,p).
edge(s,q).  edge(s,x).  edge(s,y).              edge(s,p).
edge(t,q).  edge(t,x).              edge(t,z).  edge(t,p).
edge(u,q).  edge(u,x).                          edge(u,p).
edge(v,q).  edge(v,x).  edge(v,y).  edge(v,z).  edge(v,p).


edge(1,l).  edge(1,m).  edge(1,n).  edge(1,o).  edge(1,w).
edge(2,l).  edge(2,m).  edge(2,n).  edge(2,o).  edge(2,w).
edge(3,l).  edge(3,m).  edge(3,n).  edge(3,o).  edge(3,w).
edge(4,l).  edge(4,m).  edge(4,n).  edge(4,o).  edge(4,w).
edge(5,l).  edge(5,m).  edge(5,n).  edge(5,o).  edge(5,w).
