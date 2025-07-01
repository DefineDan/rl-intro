WEB_DIR=web

.PHONY: setup setup-python setup-python-pip setup-svelte build build-python build-svelte

setup-python:
	uv sync --extra dev

setup-python-pip:
	pip install -e ".[dev]"

setup-svelte:
	cd $(WEB_DIR) && npm install

setup: setup-python setup-svelte

build-python:
	uv build

build-svelte:
	cd $(WEB_DIR) && npm run build

build: build-python build-svelte

run-web:
	cd $(WEB_DIR) && npm run dev -- --open
