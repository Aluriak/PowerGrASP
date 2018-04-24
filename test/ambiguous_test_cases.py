"""List of compression cases.

"""

cases = {}  # filename: {expected bubble}

# Expected results of tested cases
cases['multiple-optimals.lp'] = {
    'common': """
NODE\ta
NODE\ta1
NODE\ta2
NODE\ta3
NODE\tb
NODE\tb1
NODE\tb2
NODE\tb3
NODE\tc1
NODE\tc2
NODE\tc3
NODE\td1
NODE\td2
NODE\td3
NODE\te1
NODE\te2
NODE\te3
NODE\tf1
NODE\tf2
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
SET\tPWRN-a-3-1\t1.0
SET\tPWRN-a-3-2\t1.0
SET\tPWRN-a-4-1\t1.0
SET\tPWRN-a-4-2\t1.0
IN\tf1\tPWRN-a-4-2
IN\tf2\tPWRN-a-4-2
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
EDGE\tPWRN-a-3-1\tPWRN-a-3-2\t1.0
EDGE\tPWRN-a-4-1\tPWRN-a-4-2\t1.0
EDGE\ta\ta1\t1.0
EDGE\ta\ta2\t1.0
EDGE\ta\ta3\t1.0
""",
    'values': (1, 2, 3),
    'variant': """
IN\ta1\tPWRN-a-{a}-1
IN\ta2\tPWRN-a-{b}-1
IN\ta3\tPWRN-a-{c}-1
IN\ta\tPWRN-a-4-1
IN\tb1\tPWRN-a-{a}-1
IN\tb2\tPWRN-a-{b}-1
IN\tb3\tPWRN-a-{c}-1
IN\tb\tPWRN-a-4-1
IN\tc1\tPWRN-a-{a}-2
IN\tc2\tPWRN-a-{b}-2
IN\tc3\tPWRN-a-{c}-2
IN\td1\tPWRN-a-{a}-2
IN\td2\tPWRN-a-{b}-2
IN\td3\tPWRN-a-{c}-2
IN\te1\tPWRN-a-{a}-2
IN\te2\tPWRN-a-{b}-2
IN\te3\tPWRN-a-{c}-2
IN\tf1\tPWRN-a-4-2
IN\tf2\tPWRN-a-4-2
""",
}

cases['test.gml'] = {
    'common': """
NODE\tb
NODE\tc
NODE\td
NODE\tf
NODE\tg
NODE\tl
NODE\tm
NODE\tp
NODE\ts
NODE\tv
NODE\tw
""",
    'values': (1, 2),
    'variant': """
IN\tc\tPWRN-b-1-1
IN\tb\tPWRN-b-1-1
IN\tw\tPWRN-b-1-1
IN\td\tPWRN-b-1-1
IN\ts\tPWRN-b-1-1
IN\tg\tPWRN-b-2-{a}
IN\tf\tPWRN-b-2-{a}
IN\tPWRN-b-3-{a}\tPWRN-b-2-{a}
IN\tv\tPWRN-b-3-{a}
IN\tm\tPWRN-b-3-{a}
SET\tPWRN-b-1-1\t1.0
SET\tPWRN-b-2-{a}\t1.0
SET\tPWRN-b-3-{a}\t1.0
EDGE\tPWRN-b-2-{a}\tb\t1.0
EDGE\tc\tf\t1.0
EDGE\tPWRN-b-1-1\tPWRN-b-1-1\t1.0
EDGE\tm\tv\t1.0
EDGE\tl\tp\t1.0
EDGE\tPWRN-b-3-{a}\tl\t1.0
""",
}
