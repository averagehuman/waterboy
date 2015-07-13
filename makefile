
SHELL := /bin/bash

MONGO_RUNNING := $(shell if $$(pgrep mongod &>/dev/null); then echo 1; else echo 0; fi)
REDIS_RUNNING := $(shell if $$(pgrep redis-server &>/dev/null); then echo 1; else echo 0; fi)

VIRTUAL_ENV ?= $$(pwd)/env
ENV := $(VIRTUAL_ENV)
PYTHON := $(ENV)/bin/python
PIP := $(ENV)/bin/pip
TOX := $(ENV)/bin/tox

export VIRTUAL_ENV
export MONGO_RUNNING
export REDIS_RUNNING

.PHONY: venv
venv:
	@if [ ! -e $(ENV) ]; then virtualenv $(ENV); fi
	@if [ ! -e $(PIP) ]; then echo "pip not found in environment - $(ENV)"; exit 1; fi
	@if [ ! -e $(TOX) ]; then \
		echo "Installing tox in $(ENV)"; \
		$(PIP) install tox; \
	fi

.PHONY: buildout
buildout: venv
	@mkdir -p .buildout
	@if [ ! -e ".buildout/installed.cfg" ]; then \
		$(PYTHON) bootstrap.py; \
	fi;
	@./bin/buildout

.PHONY: mongo
mongo:
	@./bin/mongod.sh

.PHONY: mongo.init
mongo.init:
	@./bin/mongo --eval "rs.initiate({ _id:'rs0', members:[{_id:0, host: 'localhost:27017'}]})"

.PHONY: redis
redis:
	@./bin/redis-server

.PHONY: test
test: venv
	@$(TOX)

.PHONY: shell
shell:
	@./bin/python

.PHONY: clean
clean:
	@rm -rf .tox
	@rm -rf .buildout
	@rm -rf *.egg-info

.PHONY: environ
environ:
	@echo "VIRTUAL_ENV: $(ENV)"
	@echo -n "MONGO_RUNNING: "
	@if [ $(MONGO_RUNNING) -eq 0 ]; then echo "no"; else echo "yes"; fi
	@echo -n "REDIS_RUNNING: "
	@if [ $(REDIS_RUNNING) -eq 0 ]; then echo "no"; else echo "yes"; fi


