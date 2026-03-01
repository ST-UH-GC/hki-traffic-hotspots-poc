PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

RAW_URL := https://www.hel.fi/static/avoindata/kymp/liikenneonnettomuudet_Helsingissa.csv
RAW_CSV := data/raw/liikenneonnettomuudet_Helsingissa.csv

.PHONY: help setup download clean-data map all

help:
	@echo "Targets:"
	@echo "  make setup      - create local venv and install deps"
	@echo "  make download   - download raw Helsinki accidents CSV"
	@echo "  make clean-data - create processed accidents_clean.csv"
	@echo "  make map        - build hotspots.csv and interactive map HTML"
	@echo "  make all        - run download + clean-data + map"

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

download:
	mkdir -p data/raw
	curl -L --fail -o "$(RAW_CSV)" "$(RAW_URL)"

clean-data:
	$(PY) src/prepare_clean_data.py

map:
	$(PY) src/build_hotspots_map.py

all: download clean-data map
