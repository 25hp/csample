SHELL := /bin/bash

init:
	python setup.py develop

publish:
	python setup.py sdist upload

html:
	(cd docs && $(MAKE) html)

test:
	nosetests --with-doctest

clean:
	git clean -Xfd
