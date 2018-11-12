% a general star
edge(a,(b;c;d;e;f;g;h;i;j;k)).

% Small independant biclique
edge((b;c),(d;e)).

% a star
edge(f,(g;h;i)).

% overlapping with a biclique
edge((f;g;h),(i;j;k)).
