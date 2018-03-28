

all:
	python poc.py
	cat out/out_1.bbl
	python -m bubbletools validate out/out_1.bbl
	cp out/out_1.bbl ~/packages/PowerGrASP/powergrasp/data



t:
	pytest *.py --doctest-module -vv
