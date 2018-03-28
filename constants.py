"""Some constants to tune the compression behavior.

Mostly used for dev and debug.

"""


# run some integrity tests at some points. May slow the compression a lot.
TEST_INTEGRITY = True

# show full trace of the compression. Useful for debugging.
SHOW_STORY = True

# Recover covered edges from ASP. If falsy, will ask motif searcher to compute the edges, which may be quicker.
COVERED_EDGES_FROM_ASP = False
