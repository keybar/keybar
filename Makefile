.PHONY: help clean deps develop docs clean-build lint test test-coverage test-all
PYTEST_OPTS=-vs
COVER=bilor
APP=src/

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "develop - install all packages required for development"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "docs - generate Sphinx HTML documentation, including API docs"

clean: clean-build clean-pyc

deps:
	pip install --upgrade -r requirements.txt
	pip install -e .
	pip install "file://`pwd`#egg=keybar[tox]"
	pip install "file://`pwd`#egg=keybar[docs]"
	pip install "file://`pwd`#egg=keybar[tests]"
	pip install "file://`pwd`#egg=keybar[postgresql]"

develop: deps
	# Install ruby dependencies.
	gem install foreman compass --conservative

	if test -z "$$TRAVIS"; then pip install nodeenv && nodeenv -p; fi; \

	# Install nodejs dependencies
	npm install

	# Install bower dependencies
	bower update

docs: clean-build
	sphinx-apidoc --force -o docs/source/modules/ src/keybar src/keybar/migrations src/keybar/tests src/keybar/settings.py
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

clean-build:
	rm -fr build/ src/build
	rm -fr dist/ src/dist
	rm -fr *.egg-info src/*.egg-info
	rm -fr htmlcov/
	$(MAKE) -C docs clean

lint:
	flake8 keybar --ignore='E122,E124,E125,E126,E128,E501,F403' --exclude="**/migrations/**"

test:
	py.test ${PYTEST_OPTS} ${APP}


coverage:
	py.test --cov=${COVER} --cov-report=term-missing ${PYTEST_OPTS} ${APP}


coverage-html:
	py.test --cov=${COVER} --cov-report=html ${PYTEST_OPTS} ${APP}

tox:
	tox
