"""List of compression cases.

"""

cases = {}  # filename: expected bubble

# Expected results of tested cases
# cases['diacli.lp'] = """
# NODE	n
# NODE	r
# NODE	p
# NODE	q
# NODE	e
# NODE	b
# NODE	m
# NODE	a
# NODE	o
# NODE	c
# NODE	j
# NODE	d
# NODE	g
# NODE	l
# NODE	s
# NODE	f
# IN	l	PWRN-1-3-1
# IN	s	PWRN-1-3-1
# IN	p	PWRN-1-3-1
# IN	q	PWRN-1-4-2
# IN	o	PWRN-1-4-2
# IN	m	PWRN-1-4-1
# IN	n	PWRN-1-4-1
# IN	g	PWRN-1-1-1
# IN	PWRN-1-3-1	PWRN-1-1-1
# IN	r	PWRN-1-1-1
# IN	j	PWRN-1-1-1
# IN	f	PWRN-1-1-1
# IN	PWRN-1-4-1	PWRN-1-3-2
# IN	a	PWRN-1-2-1
# IN	d	PWRN-1-2-1
# IN	e	PWRN-1-2-2
# IN	b	PWRN-1-2-2
# IN	PWRN-1-4-2	PWRN-1-2-2
# IN	c	PWRN-1-2-2
# EDGE	PWRN-1-3-1	PWRN-1-3-2	1.0
# EDGE	PWRN-1-1-1	PWRN-1-1-1	1.0
# EDGE	PWRN-1-4-1	PWRN-1-4-2	1.0
# EDGE	b	c	1.0
# EDGE	PWRN-1-2-1	PWRN-1-2-2	1.0
# EDGE	m	n	1.0
# """

# cases['partition.lp'] = """
# NODE\ta
# NODE\tb
# NODE\tc
# NODE\td
# NODE\te
# NODE\tf
# NODE\tg
# NODE\th
# NODE\ti
# IN\tc\tPWRN-1-2-1
# IN\td\tPWRN-1-2-1
# IN\tg\tPWRN-1-2-2
# IN\th\tPWRN-1-2-2
# IN\ta\tPWRN-1-1-1
# IN\tb\tPWRN-1-1-1
# IN\ti\tPWRN-1-1-1
# IN\te\tPWRN-1-1-2
# IN\tPWRN-1-2-2\tPWRN-1-1-2
# IN\tf\tPWRN-1-1-2
# EDGE\tPWRN-1-2-1\tPWRN-1-2-2\t1.0
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# """

# cases['double_biclique_unambiguous.lp'] = """
# NODE\td2
# NODE\th
# NODE\tn
# NODE\tq
# NODE\te
# NODE\tc
# NODE\td
# NODE\ti
# NODE\tm2
# NODE\tg
# NODE\tp
# NODE\tf1
# NODE\tb2
# NODE\ta
# NODE\tf2
# NODE\tj
# NODE\tb1
# NODE\tm
# NODE\to
# NODE\tl
# IN\tf2\tPWRN-1-2-1
# IN\tj\tPWRN-1-2-1
# IN\tg\tPWRN-1-2-1
# IN\tf1\tPWRN-1-2-1
# IN\tPWRN-1-3-1\tPWRN-1-2-1
# IN\tm\tPWRN-1-5-1
# IN\tm2\tPWRN-1-5-1
# IN\tPWRN-1-4-1\tPWRN-1-3-2
# IN\td2\tPWRN-1-1-1
# IN\td\tPWRN-1-1-1
# IN\ta\tPWRN-1-1-1
# IN\tq\tPWRN-1-1-2
# IN\te\tPWRN-1-1-2
# IN\tc\tPWRN-1-1-2
# IN\tb2\tPWRN-1-1-2
# IN\tb1\tPWRN-1-1-2
# IN\to\tPWRN-1-1-2
# IN\tp\tPWRN-1-3-1
# IN\tl\tPWRN-1-3-1
# IN\th\tPWRN-1-2-2
# IN\ti\tPWRN-1-2-2
# IN\tPWRN-1-5-1\tPWRN-1-4-1
# IN\tn\tPWRN-1-4-1
# EDGE\tPWRN-1-5-1\tn\t1.0
# EDGE\tPWRN-1-2-1\tPWRN-1-2-2\t1.0
# EDGE\tf1\tg\t1.0
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# EDGE\tPWRN-1-3-1\tPWRN-1-3-2\t1.0
# EDGE\tPWRN-1-4-1\tq\t1.0
# EDGE\tb1\tc\t1.0
# """


# cases['testblocks.lp'] = """
# NODE\tf
# NODE\td
# NODE\tm
# NODE\ti
# NODE\ta
# NODE\th
# NODE\te
# NODE\tg
# NODE\tc
# NODE\tb
# NODE\tj
# IN\te\tPWRN-1-2-1
# IN\tPWRN-1-3-1\tPWRN-1-2-1
# IN\ta\tPWRN-1-3-1
# IN\tc\tPWRN-1-3-1
# IN\tb\tPWRN-1-3-1
# IN\td\tPWRN-1-3-1
# IN\tg\tPWRN-1-4-1
# IN\tf\tPWRN-1-4-1
# IN\th\tPWRN-1-4-1
# IN\ti\tPWRN-1-1-1
# IN\tj\tPWRN-1-1-1
# IN\tPWRN-1-4-1\tPWRN-1-1-1
# IN\tm\tPWRN-1-1-1
# EDGE\tPWRN-1-2-1\tPWRN-1-2-1\t1.0
# EDGE\tPWRN-1-3-1\tf\t1.0
# EDGE\tPWRN-1-4-1\tl\t1.0
# EDGE\tPWRN-1-1-1\tPWRN-1-1-1\t1.0
# """

cases['pnode-to-clique.lp'] = """
NODE\tb
NODE\td
NODE\ta
NODE\tf
NODE\te
NODE\tc
IN\te\tPWRN-1-2-1
IN\tc\tPWRN-1-2-1
IN\td\tPWRN-1-2-1
IN\tPWRN-1-2-1\tPWRN-1-1-2
IN\ta\tPWRN-1-1-1
IN\tf\tPWRN-1-1-1
IN\tb\tPWRN-1-1-1
EDGE\tPWRN-1-2-1\tPWRN-1-2-1\t1.0
EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
"""

cases['clique.lp'] = """
NODE\tc
NODE\tb
NODE\ta
NODE\td
IN\tc\tPWRN-1-1-1
IN\tb\tPWRN-1-1-1
IN\ta\tPWRN-1-1-1
IN\td\tPWRN-1-1-1
EDGE\tPWRN-1-1-1\tPWRN-1-1-1\t1.0
"""

cases['star.lp'] = """
NODE\tc
NODE\td
NODE\tb
NODE\te
IN\tc\tPWRN-1-1-2
IN\td\tPWRN-1-1-2
IN\tb\tPWRN-1-1-2
IN\te\tPWRN-1-1-2
EDGE\ta\tPWRN-1-1-2\t1.0
"""

# cases['concomp.lp'] = """
# EDGE\t23\t42\t1.0
# NODE\t2
# NODE\t5
# NODE\t3
# NODE\t4
# NODE\t6
# NODE\t1
# IN\t1\tPWRN-1-1-1
# IN\t6\tPWRN-1-1-1
# IN\t4\tPWRN-1-1-2
# IN\t2\tPWRN-1-1-2
# IN\t5\tPWRN-1-1-2
# IN\t3\tPWRN-1-1-2
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# NODE\tb
# NODE\tc
# NODE\td
# NODE\te
# IN\tb\tPWRN-1-1-2
# IN\tc\tPWRN-1-1-2
# IN\td\tPWRN-1-1-2
# IN\te\tPWRN-1-1-2
# EDGE\ta\tPWRN-1-1-2\t1.0
# """

# cases['prio_deg.lp'] = """
# NODE\tc
# NODE\te
# NODE\tf
# NODE\td
# NODE\th
# NODE\tg
# NODE\tb
# NODE\ta
# IN\tg\tPWRN-1-2-1
# IN\tf\tPWRN-1-2-1
# IN\th\tPWRN-1-2-1
# IN\tc\tPWRN-1-1-1
# IN\tb\tPWRN-1-1-1
# IN\ta\tPWRN-1-1-1
# IN\te\tPWRN-1-1-2
# IN\td\tPWRN-1-1-2
# EDGE\tPWRN-1-2-1\ts\t1.0
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# EDGE\ta\ts\t1.0
# """

# cases['perfectfit.lp'] = """
# NODE\tj
# NODE\tl
# NODE\tb
# NODE\tg
# NODE\th
# NODE\ta
# NODE\td
# NODE\tc
# NODE\te
# NODE\tf
# NODE\ti
# IN\tPWRN-1-2-1\tPWRN-1-1-2
# IN\th\tPWRN-1-1-2
# IN\ti\tPWRN-1-1-2
# IN\tb\tPWRN-1-1-1
# IN\tPWRN-1-3-1\tPWRN-1-1-1
# IN\ta\tPWRN-1-1-1
# IN\tj\tPWRN-1-3-2
# IN\tl\tPWRN-1-3-2
# IN\td\tPWRN-1-3-1
# IN\tc\tPWRN-1-3-1
# IN\te\tPWRN-1-2-1
# IN\tg\tPWRN-1-2-1
# IN\tf\tPWRN-1-2-1
# IN\tPWRN-1-3-2\tPWRN-1-2-2
# EDGE\tPWRN-1-3-1\tPWRN-1-3-2\t1.0
# EDGE\tPWRN-1-2-1\tPWRN-1-2-2\t1.0
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# """

# cases['ecoli_2896-53.gml'] = """
# NODE\tR_VALabc
# NODE\tR_DHAD1
# NODE\tR_VALt2r
# IN\tR_VALabc\tPWRN-R_DHAD1-1-1
# IN\tR_DHAD1\tPWRN-R_DHAD1-1-1
# IN\tR_VALt2r\tPWRN-R_DHAD1-1-1
# EDGE\tPWRN-R_DHAD1-1-1\tPWRN-R_DHAD1-1-1\t1.0
# NODE\tRXN-14213
# NODE\tRXN-14200
# NODE\tR_DTMPK
# IN\tRXN-14213\tPWRN-RXN-14200-1-1
# IN\tRXN-14200\tPWRN-RXN-14200-1-1
# IN\tR_DTMPK\tPWRN-RXN-14200-1-1
# EDGE\tPWRN-RXN-14200-1-1\tPWRN-RXN-14200-1-1\t1.0
# NODE\tR_EX_26dap_M_LPAREN_e_RPAREN_
# NODE\tRXN-14246
# NODE\tR_DAPE
# IN\tR_EX_26dap_M_LPAREN_e_RPAREN_\tPWRN-RXN-14246-1-1
# IN\tRXN-14246\tPWRN-RXN-14246-1-1
# IN\tR_DAPE\tPWRN-RXN-14246-1-1
# EDGE\tPWRN-RXN-14246-1-1\tPWRN-RXN-14246-1-1\t1.0
# EDGE\tNADH-KINASE-RXN\tR_NADK\t1.0
# NODE\tR_G1PACT
# NODE\tGLUCOSAMINEPNACETYLTRANS-RXN
# NODE\tR_PGAMT
# NODE\tPHOSACETYLGLUCOSAMINEMUT-RXN
# NODE\tR_AMANAPE
# NODE\tR_EX_acgam_LPAREN_e_RPAREN_
# IN\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-2-1\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-1-1
# IN\tPHOSACETYLGLUCOSAMINEMUT-RXN\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-1-1
# IN\tGLUCOSAMINEPNACETYLTRANS-RXN\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-2-1
# IN\tR_AMANAPE\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-2-1
# IN\tR_EX_acgam_LPAREN_e_RPAREN_\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-2-1
# IN\tR_G1PACT\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-1-2
# IN\tR_PGAMT\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-1-2
# EDGE\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-1-1\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-1-2\t1.0
# EDGE\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-2-1\tPWRN-GLUCOSAMINEPNACETYLTRANS-RXN-2-1\t1.0
# NODE\tR_GLGC
# NODE\tRXN-10770
# NODE\tGLYMALTOPHOSPHORYL-RXN
# IN\tR_GLGC\tPWRN-GLYMALTOPHOSPHORYL-RXN-1-1
# IN\tRXN-10770\tPWRN-GLYMALTOPHOSPHORYL-RXN-1-1
# IN\tGLYMALTOPHOSPHORYL-RXN\tPWRN-GLYMALTOPHOSPHORYL-RXN-1-1
# EDGE\tPWRN-GLYMALTOPHOSPHORYL-RXN-1-1\tPWRN-GLYMALTOPHOSPHORYL-RXN-1-1\t1.0
# """

# cases['test.gml'] = """
# NODE\tg
# NODE\tb
# NODE\tm
# NODE\ts
# NODE\td
# NODE\tv
# NODE\tw
# NODE\tf
# NODE\tc
# IN\td\tPWRN-b-1-1
# IN\tw\tPWRN-b-1-1
# IN\tc\tPWRN-b-1-1
# IN\ts\tPWRN-b-1-1
# IN\tb\tPWRN-b-1-1
# IN\tf\tPWRN-b-2-2
# IN\tPWRN-b-3-2\tPWRN-b-2-2
# IN\tg\tPWRN-b-2-2
# IN\tm\tPWRN-b-3-2
# IN\tv\tPWRN-b-3-2
# EDGE\tl\tPWRN-b-3-2\t1.0
# EDGE\tl\tp\t1.0
# EDGE\tPWRN-b-1-1\tPWRN-b-1-1\t1.0
# EDGE\tm\tv\t1.0
# EDGE\tc\tf\t1.0
# EDGE\tb\tPWRN-b-2-2\t1.0
# """

# cases['unclique.lp'] = """
# NODE\td
# NODE\te
# NODE\ta
# NODE\th
# NODE\tg
# NODE\ti
# NODE\tc
# NODE\tb
# NODE\tf
# IN\tc\tPWRN-1-1-1
# IN\te\tPWRN-1-1-1
# IN\tf\tPWRN-1-1-1
# IN\tg\tPWRN-1-1-1
# IN\th\tPWRN-1-1-2
# IN\ti\tPWRN-1-1-2
# IN\tPWRN-1-3-1\tPWRN-1-2-1
# IN\td\tPWRN-1-3-1
# IN\tb\tPWRN-1-3-1
# IN\ta\tPWRN-1-3-1
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# EDGE\tPWRN-1-2-1\tc\t1.0
# EDGE\tPWRN-1-3-1\tPWRN-1-3-1\t1.0
# """

# cases['order.lp'] = """
# NODE\t4
# NODE\ta
# NODE\t6
# NODE\t5
# IN\t4\tPWRN-4-1-1
# IN\ta\tPWRN-4-1-1
# IN\t6\tPWRN-4-1-1
# IN\t5\tPWRN-4-1-1
# EDGE\ta\ta\t1.0
# EDGE\tPWRN-4-1-1\t10\t1.0
# """

# cases['test.graphml'] = """
# NODE\t2
# NODE\t3
# NODE\t1
# NODE\t4
# IN\t1\tPWRN-1-1-1
# IN\t4\tPWRN-1-1-1
# IN\t3\tPWRN-1-1-2
# IN\t2\tPWRN-1-1-2
# EDGE\tPWRN-1-1-1\tPWRN-1-1-2\t1.0
# """

# cases['one_edge.lp'] = """
# EDGE\ta\tb\t1.0
# """

# cases['test.gml'] = """
# NODE\tc
# NODE\tw
# NODE\tf
# NODE\tv
# NODE\ts
# NODE\tb
# NODE\td
# NODE\tg
# NODE\tm
# IN\tc\tPWRN-b-1-1
# IN\tb\tPWRN-b-1-1
# IN\tw\tPWRN-b-1-1
# IN\td\tPWRN-b-1-1
# IN\ts\tPWRN-b-1-1
# IN\tg\tPWRN-b-2-2
# IN\tf\tPWRN-b-2-2
# IN\tPWRN-b-3-2\tPWRN-b-2-2
# IN\tv\tPWRN-b-3-2
# IN\tm\tPWRN-b-3-2
# EDGE\tb\tPWRN-b-2-2\t1.0
# EDGE\tc\tf\t1.0
# EDGE\tPWRN-b-1-1\tPWRN-b-1-1\t1.0
# EDGE\tm\tv\t1.0
# EDGE\tl\tp\t1.0
# EDGE\tl\tPWRN-b-3-2\t1.0
# """

# cases['horrible_data.lp'] = """
# EDGE\t"$PYTHONPATH"\t"[a,b]"\t1.0
# NODE\t"'echo coucou'"
# NODE\t"\"echo coucou\""
# IN\t"'echo coucou'"\tPWRN-"\"echo coucou\""-1-1
# IN\t"\"echo coucou\""\tPWRN-"\"echo coucou\""-1-1
# EDGE\tPWRN-"\"echo coucou\""-1-1\t[a]\t1.0
# EDGE\t"\"echo coucou\""\t[a]\t1.0
# """
