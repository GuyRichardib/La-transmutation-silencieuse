count:
	python3 scripts/wordcount.py

build:
	bash scripts/build.sh

syntony:
	python3 scripts/syntony_guard.py

release:
	git tag -a v$$(date +%Y.%m.%d) -m "Draft release"
	git push --tags
