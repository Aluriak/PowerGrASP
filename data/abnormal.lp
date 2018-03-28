% This network raises an abnormal situation multiple times:
edge("YNL069C","YOR063W").
edge("YBL087C","YGL031C").
edge("YER117W","YGL031C").
edge("YIL133C","YNL067W").
edge("YGL147C","YNL069C").
edge("YBL087C","YOR063W").
edge("YGR148C","YOR063W").
edge("YNL067W","YNL069C").
edge("YGL147C","YIL133C").
edge("YIL133C","YOR063W").
edge("YER117W","YGR148C").
edge("YER117W","YOR063W").
edge("YBL087C","YGR148C").
edge("YGL031C","YOR063W").
edge("YGL147C","YNL067W").

% The same, but with letter (easier to debug):
edge(b,c).
edge(a,d).
edge(e,d).
edge(f,g).
edge(h,b).
edge(a,c).
edge(i,c).
edge(g,b).
edge(h,f).
edge(f,c).
edge(e,i).
edge(e,c).
edge(a,i).
edge(d,c).
edge(h,g).
