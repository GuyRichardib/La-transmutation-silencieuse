count:
	python3 scripts/wordcount.py

build:
	bash scripts/build.sh

release:
	git tag -a v$$(date +%Y.%m.%d) -m "Draft release"
	git push --tags
