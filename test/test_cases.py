"""List of compression cases.

"""

cases = {}  # filename: expected bubble

# Expected results of tested cases
cases['diacli.lp'] = """
NODE\tn
NODE\tr
NODE\tp
NODE\tq
NODE\te
NODE\tb
NODE\tm
NODE\ta
NODE\to
NODE\tc
NODE\tj
NODE\td
NODE\tg
NODE\tl
NODE\ts
NODE\tf
IN\tPWRN-a-3-1\tPWRN-a-1-1
IN\tPWRN-a-4-2\tPWRN-a-2-2
IN\ta\tPWRN-a-2-1
IN\tb\tPWRN-a-2-2
IN\tc\tPWRN-a-2-2
IN\td\tPWRN-a-2-1
IN\te\tPWRN-a-2-2
IN\tf\tPWRN-a-1-1
IN\tg\tPWRN-a-1-1
IN\tj\tPWRN-a-1-1
IN\tl\tPWRN-a-3-1
IN\tm\tPWRN-a-3-2
IN\tn\tPWRN-a-3-2
IN\to\tPWRN-a-4-2
IN\tp\tPWRN-a-3-1
IN\tq\tPWRN-a-4-2
IN\tr\tPWRN-a-1-1
IN\ts\tPWRN-a-3-1
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
SET\tPWRN-a-3-1\t1.0
SET\tPWRN-a-3-2\t1.0
SET\tPWRN-a-3-2\t1.0
SET\tPWRN-a-4-2\t1.0
EDGE\tPWRN-a-3-1\tPWRN-a-3-2\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-1\t1.0
EDGE\tPWRN-a-3-2\tPWRN-a-4-2\t1.0
EDGE\tb\tc\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
EDGE\tm\tn\t1.0
"""

cases['partition.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ti
IN\tc\tPWRN-a-2-1
IN\td\tPWRN-a-2-1
IN\tg\tPWRN-a-2-2
IN\th\tPWRN-a-2-2
IN\ta\tPWRN-a-1-1
IN\tb\tPWRN-a-1-1
IN\ti\tPWRN-a-1-1
IN\te\tPWRN-a-1-2
IN\tPWRN-a-2-2\tPWRN-a-1-2
IN\tf\tPWRN-a-1-2
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
"""

cases['double_biclique_unambiguous.lp'] = """
NODE\ta
NODE\tb1
NODE\tb2
NODE\tc
NODE\td
NODE\td2
NODE\te
NODE\tf1
NODE\tf2
NODE\tg
NODE\th
NODE\ti
NODE\tj
NODE\tl
NODE\tm
NODE\tm2
NODE\tn
NODE\to
NODE\tp
NODE\tq
IN\tPWRN-a-3-1\tPWRN-a-2-1
IN\tPWRN-a-5-1\tPWRN-a-3-2
IN\ta\tPWRN-a-1-1
IN\tb1\tPWRN-a-1-2
IN\tb2\tPWRN-a-1-2
IN\tc\tPWRN-a-1-2
IN\td2\tPWRN-a-1-1
IN\td\tPWRN-a-1-1
IN\te\tPWRN-a-1-2
IN\tf1\tPWRN-a-2-1
IN\tf2\tPWRN-a-2-1
IN\tg\tPWRN-a-2-1
IN\th\tPWRN-a-2-2
IN\ti\tPWRN-a-2-2
IN\tj\tPWRN-a-2-1
IN\tl\tPWRN-a-3-1
IN\tm2\tPWRN-a-5-1
IN\tm\tPWRN-a-5-1
IN\tn\tPWRN-a-3-2
IN\to\tPWRN-a-1-2
IN\tp\tPWRN-a-3-1
IN\tq\tPWRN-a-1-2
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
SET\tPWRN-a-3-1\t1.0
SET\tPWRN-a-3-2\t1.0
SET\tPWRN-a-5-1\t1.0
EDGE\tPWRN-a-5-1\tn\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
EDGE\tf1\tg\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-3-1\tPWRN-a-3-2\t1.0
EDGE\tPWRN-a-3-2\tq\t1.0
EDGE\tb1\tc\t1.0
"""


cases['testblocks.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ti
NODE\tj
NODE\tl
NODE\tm
IN\te\tPWRN-a-2-1
IN\tPWRN-a-3-1\tPWRN-a-2-1
IN\ta\tPWRN-a-3-1
IN\tc\tPWRN-a-3-1
IN\tb\tPWRN-a-3-1
IN\td\tPWRN-a-3-1
IN\tg\tPWRN-a-4-1
IN\tf\tPWRN-a-4-1
IN\th\tPWRN-a-4-1
IN\ti\tPWRN-a-1-1
IN\tj\tPWRN-a-1-1
IN\tPWRN-a-4-1\tPWRN-a-1-1
IN\tm\tPWRN-a-1-1
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-3-1\t1.0
SET\tPWRN-a-4-1\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-1\t1.0
EDGE\tPWRN-a-3-1\tf\t1.0
EDGE\tPWRN-a-4-1\tl\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-1\t1.0
"""

cases['pnode-to-clique.lp'] = """
NODE\tb
NODE\td
NODE\ta
NODE\tf
NODE\te
NODE\tc
IN\te\tPWRN-a-1-2
IN\tc\tPWRN-a-1-2
IN\td\tPWRN-a-1-2
IN\ta\tPWRN-a-1-1
IN\tf\tPWRN-a-1-1
IN\tb\tPWRN-a-1-1
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-1-1\t1.0
EDGE\tPWRN-a-1-2\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
"""

cases['clique.lp'] = """
NODE\tc
NODE\tb
NODE\ta
NODE\td
IN\tc\tPWRN-a-1-1
IN\tb\tPWRN-a-1-1
IN\ta\tPWRN-a-1-1
IN\td\tPWRN-a-1-1
SET\tPWRN-a-1-1\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-1\t1.0
"""

cases['star.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
IN\tc\tPWRN-a-1-2
IN\td\tPWRN-a-1-2
IN\tb\tPWRN-a-1-2
IN\te\tPWRN-a-1-2
SET\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-1-2\ta\t1.0
"""

cases['concomp.lp'] = """
NODE\t23
NODE\t42
EDGE\t23\t42\t1.0
NODE\t1
NODE\t2
NODE\t3
NODE\t4
NODE\t5
NODE\t6
IN\t1\tPWRN-1-1-1
IN\t2\tPWRN-1-1-2
IN\t3\tPWRN-1-1-2
IN\t4\tPWRN-1-1-2
IN\t5\tPWRN-1-1-2
IN\t6\tPWRN-1-1-1
SET\tPWRN-1-1-1\t1.0
SET\tPWRN-1-1-2\t1.0
EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
IN\tb\tPWRN-a-1-2
IN\tc\tPWRN-a-1-2
IN\td\tPWRN-a-1-2
IN\te\tPWRN-a-1-2
SET\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-1-2\ta\t1.0
"""

cases['prio_deg.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ts
IN\tg\tPWRN-a-2-1
IN\tf\tPWRN-a-2-1
IN\th\tPWRN-a-2-1
IN\tc\tPWRN-a-1-1
IN\tb\tPWRN-a-1-1
IN\ta\tPWRN-a-1-1
IN\te\tPWRN-a-1-2
IN\td\tPWRN-a-1-2
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
EDGE\tPWRN-a-2-1\ts\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
EDGE\ta\ts\t1.0
"""

cases['perfectfit.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ti
NODE\tj
NODE\tl
IN\tPWRN-a-2-1\tPWRN-a-1-2
IN\tb\tPWRN-a-1-1
IN\th\tPWRN-a-1-2
IN\ti\tPWRN-a-1-2
IN\tPWRN-a-3-1\tPWRN-a-1-1
IN\ta\tPWRN-a-1-1
IN\tc\tPWRN-a-3-1
IN\td\tPWRN-a-3-1
IN\te\tPWRN-a-2-1
IN\tf\tPWRN-a-2-1
IN\tg\tPWRN-a-2-1
IN\tj\tPWRN-a-2-2
IN\tl\tPWRN-a-2-2
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
SET\tPWRN-a-3-1\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
EDGE\tPWRN-a-2-2\tPWRN-a-3-1\t1.0
"""

cases['variable-name.gml'] = """
NODE\tA
NODE\tB
NODE\tC
NODE\tD
NODE\tE
SET\tPWRN-A-1-2\t1.0
IN\tC\tPWRN-A-1-2
IN\tB\tPWRN-A-1-2
IN\tD\tPWRN-A-1-2
EDGE\tA\tPWRN-A-1-2\t1.0
EDGE\tB\tE\t1.0
"""

cases['unclique.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ti
IN\tc\tPWRN-a-1-1
IN\te\tPWRN-a-1-1
IN\tf\tPWRN-a-1-1
IN\tg\tPWRN-a-1-1
IN\th\tPWRN-a-1-2
IN\ti\tPWRN-a-1-2
IN\td\tPWRN-a-2-1
IN\tb\tPWRN-a-2-1
IN\ta\tPWRN-a-2-1
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-2-1\tc\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-1\t1.0
"""

cases['order.lp'] = """
NODE\tb
NODE\t10
NODE\t4
NODE\t5
NODE\t6
NODE\ta
IN\t4\tPWRN-a-1-1
IN\ta\tPWRN-a-1-1
IN\t6\tPWRN-a-1-1
IN\t5\tPWRN-a-1-1
SET\tPWRN-a-1-1\t1.0
EDGE\ta\tb\t1.0
EDGE\t10\tPWRN-a-1-1\t1.0
"""

cases['quoting.lp'] = """
NODE\ta
NODE\tb
NODE\tc
IN\tc\tPWRN-a-1-2
IN\tb\tPWRN-a-1-2
SET\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-1-2\ta\t1.0
"""

cases['test.graphml'] = """
NODE\t1
NODE\t2
NODE\t3
NODE\t4
IN\t1\tPWRN-1-1-1
IN\t4\tPWRN-1-1-1
IN\t3\tPWRN-1-1-2
IN\t2\tPWRN-1-1-2
SET\tPWRN-1-1-1\t1.0
SET\tPWRN-1-1-2\t1.0
EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
"""

cases['one_edge.lp'] = """
NODE\ta
NODE\tb
EDGE\ta\tb\t1.0
"""

cases['test.gml'] = """
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
IN\tc\tPWRN-b-1-1
IN\tb\tPWRN-b-1-1
IN\tw\tPWRN-b-1-1
IN\td\tPWRN-b-1-1
IN\ts\tPWRN-b-1-1
IN\tg\tPWRN-b-2-2
IN\tf\tPWRN-b-2-2
IN\tPWRN-b-3-2\tPWRN-b-2-2
IN\tv\tPWRN-b-3-2
IN\tm\tPWRN-b-3-2
SET\tPWRN-b-1-1\t1.0
SET\tPWRN-b-2-2\t1.0
SET\tPWRN-b-3-2\t1.0
EDGE\tPWRN-b-2-2\tb\t1.0
EDGE\tc\tf\t1.0
EDGE\tPWRN-b-1-1\tPWRN-b-1-1\t1.0
EDGE\tm\tv\t1.0
EDGE\tl\tp\t1.0
EDGE\tPWRN-b-3-2\tl\t1.0
"""

cases['horrible_data.lp'] = """
NODE\t_c92__c34_echo_c32_coucou_c92__c34_
NODE\t_c91_a_c93_
NODE\t_c39_echo_c32_coucou_c39_
SET\tPWRN-_c39_echo_c32_coucou_c39_-1-1\t1.0
IN\t_c92__c34_echo_c32_coucou_c92__c34_\tPWRN-_c39_echo_c32_coucou_c39_-1-1
IN\t_c39_echo_c32_coucou_c39_\tPWRN-_c39_echo_c32_coucou_c39_-1-1
EDGE\tPWRN-_c39_echo_c32_coucou_c39_-1-1\t_c91_a_c93_\t1.0
NODE\t_c91_a_c44_b_c93_
NODE\t_c36_PYTHONPATH
EDGE\t_c36_PYTHONPATH\t_c91_a_c44_b_c93_\t1.0
"""

cases['inclusions.lp'] = """
NODE\t1
NODE\t2
NODE\t3
NODE\t5
NODE\t6
NODE\t7
NODE\t8
NODE\t9
NODE\t10
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ti
NODE\tj
NODE\tk
NODE\tl
NODE\tm
NODE\tn
NODE\to
NODE\tp
NODE\tq
NODE\tr
NODE\tv
NODE\tv2
NODE\tw
NODE\tw2
IN\tPWRN-a-6-2\tPWRN-a-2-1
IN\tPWRN-a-6-1\tPWRN-a-4-1
IN\tPWRN-a-5-1\tPWRN-a-6-1
IN\tPWRN-a-4-1\tPWRN-a-1-1
IN\tPWRN-a-4-2\tPWRN-a-3-1
IN\t10\tPWRN-a-2-1
IN\t1\tPWRN-a-3-1
IN\t2\tPWRN-a-3-1
IN\t3\tPWRN-a-3-1
IN\t5\tPWRN-a-2-1
IN\t6\tPWRN-a-2-1
IN\t7\tPWRN-a-2-1
IN\t8\tPWRN-a-2-1
IN\t9\tPWRN-a-2-1
IN\ta\tPWRN-a-1-1
IN\tb\tPWRN-a-1-1
IN\tc\tPWRN-a-1-1
IN\td\tPWRN-a-4-1
IN\te\tPWRN-a-6-1
IN\tf\tPWRN-a-5-1
IN\tg\tPWRN-a-5-1
IN\th\tPWRN-a-1-1
IN\ti\tPWRN-a-1-1
IN\tj\tPWRN-a-1-1
IN\tk\tPWRN-a-1-1
IN\tl\tPWRN-a-1-1
IN\tm\tPWRN-a-4-2
IN\tn\tPWRN-a-4-2
IN\to\tPWRN-a-4-2
IN\tp\tPWRN-a-4-2
IN\tq\tPWRN-a-6-2
IN\tr\tPWRN-a-6-2
IN\tv2\tPWRN-a-5-2
IN\tv\tPWRN-a-5-2
IN\tw2\tPWRN-a-5-2
IN\tw\tPWRN-a-5-2
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-3-1\t1.0
SET\tPWRN-a-4-1\t1.0
SET\tPWRN-a-5-1\t1.0
SET\tPWRN-a-6-1\t1.0
SET\tPWRN-a-4-2\t1.0
SET\tPWRN-a-5-2\t1.0
SET\tPWRN-a-6-2\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-1\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-1\t1.0
EDGE\tPWRN-a-3-1\tPWRN-a-3-1\t1.0
EDGE\tPWRN-a-4-1\tPWRN-a-4-2\t1.0
EDGE\tPWRN-a-5-1\tPWRN-a-5-2\t1.0
EDGE\tPWRN-a-6-1\tPWRN-a-6-2\t1.0
"""

cases['disjoint-subpnodes.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
IN\ta\tPWRN-a-1-1
IN\tb\tPWRN-a-3-1
IN\tc\tPWRN-a-3-1
IN\td\tPWRN-a-2-1
IN\te\tPWRN-a-2-1
IN\tf\tPWRN-a-2-1
IN\tPWRN-a-2-1\tPWRN-a-1-1
IN\tPWRN-a-3-1\tPWRN-a-1-1
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-3-1\t1.0
EDGE\tPWRN-a-1-1\tPWRN-a-1-1\t1.0
EDGE\tPWRN-a-2-1\tg\t1.0
EDGE\tPWRN-a-3-1\th\t1.0
"""


cases['consider-included-nodes.lp'] = """
NODE\ta
NODE\tb
NODE\tc
NODE\td
NODE\te
NODE\tf
NODE\tg
NODE\th
NODE\ti
NODE\tj
NODE\tl
NODE\tm
NODE\troot
NODE\troot2
NODE\troot3
SET\tPWRN-a-1-1\t1.0
SET\tPWRN-a-1-2\t1.0
SET\tPWRN-a-2-1\t1.0
SET\tPWRN-a-2-2\t1.0
IN\tPWRN-a-2-1\tPWRN-a-1-1
IN\tPWRN-a-2-2\tPWRN-a-1-1
IN\ta\tPWRN-a-1-1
IN\tb\tPWRN-a-2-1
IN\tc\tPWRN-a-2-1
IN\td\tPWRN-a-2-2
IN\te\tPWRN-a-2-2
IN\tf\tPWRN-a-2-2
IN\tg\tPWRN-a-2-2
IN\th\tPWRN-a-2-2
IN\ti\tPWRN-a-1-1
IN\tj\tPWRN-a-1-1
IN\tl\tPWRN-a-1-1
IN\tm\tPWRN-a-1-1
IN\troot2\tPWRN-a-1-2
IN\troot3\tPWRN-a-1-2
IN\troot\tPWRN-a-1-2
EDGE\tPWRN-a-1-1\tPWRN-a-1-2\t1.0
EDGE\tPWRN-a-2-1\tPWRN-a-2-2\t1.0
EDGE\ta\tb\t1.0
EDGE\ta\td\t1.0
"""
