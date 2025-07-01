WEB_DIR=web

.PHONY: setup setup-python setup-python-pip setup-web build build-python build-web

setup-python:
	uv sync --extra dev

setup-python-pip:
	pip install -e ".[dev]"

setup-web:
	cd $(WEB_DIR) && npm install

setup: setup-python setup-web

build-python:
	uv build

build-web:
	cd $(WEB_DIR) && npm run build

build: build-python build-web
	@echo "[INFO] If you made changes to the python package, remember to overwrite the wheel in web/static/py!"

run-web:
	cd $(WEB_DIR) && npm run dev -- --open
