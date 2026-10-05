.PHONY: install dev verify

PYTHON ?= python3
VENV_BIN := $(if $(wildcard venv/bin/python),venv/bin/python,$(PYTHON))

install:
	$(PYTHON) -m venv venv
	venv/bin/pip install -r requirements.txt

dev:
	$(VENV_BIN) src/main.py

verify:
	$(VENV_BIN) -c "import sys; sys.path.insert(0,'.'); from src.main import app; print('routes:', sorted(r.rule for r in app.url_map.iter_rules()))"
