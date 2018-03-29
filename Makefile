

all:
	python main.py
	python -m bubbletools validate out/out.bbl
	cp out/out.bbl ~/packages/PowerGrASP/powergrasp/data



t:
	pytest *.py test --doctest-module -vv
