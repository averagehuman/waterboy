
VIRTUAL_ENV ?= $$(pwd)/env
PYTHON := $(VIRTUAL_ENV)/bin/python
PIP := $(VIRTUAL_ENV)/bin/pip
TOX := $(VIRTUAL_ENV)/bin/tox

.PHONY: venv
venv:
	@if [ ! -e $(VIRTUAL_ENV) ]; then virtualenv $(VIRTUAL_ENV); fi
	@if [ ! -e $(PIP) ]; then echo "pip not found in environment - $(VIRTUAL_ENV)"; exit 1; fi
	@if [ ! -e $(TOX) ]; then \
		echo "Installing tox in $(VIRTUAL_ENV)"; \
		$(PIP) install tox; \
	fi

.PHONY: test
test: venv
	@$(TOX)

.PHONY: clean
clean:
	@rm -rf .tox

