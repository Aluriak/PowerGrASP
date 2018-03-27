

all:
	python poc.py
	cat out/out_1.bbl



t:
	pytest *.py --doctest-module -vv
