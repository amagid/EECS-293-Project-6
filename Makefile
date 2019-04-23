SHELL:=/bin/bash
PROJECT:=typed_parser
all: build test

test:
	( \
		source venv/bin/activate; \
		coverage run --branch --source=${PROJECT} --omit="*test*" -m pytest ${PROJECT}/test/; \
		coverage report; \
		echo ; echo ; \
		echo "===== Methods >= 3 Complexity Below =====" ; \
		echo ; \
		find ./typed_parser/*.py | xargs -L1 python3 -m mccabe --min=4; \
		echo ; echo ; \
		echo "===== Tests > 4 Complexity Below =====" ; \
		echo ; \
		find ./typed_parser/test/*.py | xargs -L1 python3 -m mccabe --min=6; \
		echo ; echo ; \
	)

build:
	python3.6 -m venv venv
	( \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
		pip install -e .; \
	)

run:
	( \
		source venv/bin/activate; \
		./cli.py; \
	)

clean:
	rm -rf venv/
	rm -rf .tox/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf *.egg-info
	rm -rf .coverage
	find ${PROJECT} -name "__pycache__" -type d -exec rm -rf {} +

# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = TypedParser
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

docs:
	( \
		make html; \
	)

docserver:
	( \
		source venv/bin/activate; \
		cd build/html; \
		python3 -m http.server; \
	)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)