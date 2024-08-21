.DEFAULT_GOAL := help

SHELL=/bin/bash
VENV = venv

BUILD_VERSION ?= 0.1.0

# Detect the operating system and set the virtualenv bin directory
ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

py-setup: $(VENV)/bin/activate

$(VENV)/bin/activate: $(VENV)/.venv-timestamp

$(VENV)/.venv-timestamp: python/setup.py python/requirements/lint-requirements.txt
	# Create new virtual environment if requirements have changed
	python3 -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install twine wheel auditwheel
	$(VENV_BIN)/pip install -r python/requirements/lint-requirements.txt
	touch $(VENV)/.venv-timestamp

.PHONY: py-fmt
py-fmt: py-setup ## Format Python code
	$(VENV_BIN)/isort python/
	$(VENV_BIN)/black .

.PHONY: py-clean-dist
py-clean-dist: ## Clean up the distribution
	cd python && rm -rf dist/ *.egg-info build/ src/*.egg-info

.PHONY: py-package
py-package: py-clean-dist py-setup ## Package the project for distribution
	cd python && ../$(VENV_BIN)/python3 setup.py sdist bdist_wheel
	cd python/dist && mv dbgpt_tugraph_plugins-*.whl dbgpt_tugraph_plugins-${BUILD_VERSION}-py3-none-any.whl

.PHONY: py-upload
py-upload: ## Upload the package to PyPI
	cd python && ../$(VENV_BIN)/twine upload dist/*

.PHONY: help
help:  ## Display this help screen
	@echo "Available commands:"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort
	