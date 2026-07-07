# cross-platform: use python -m so Windows/PowerShell users don't need `make`
# (Makefile is a convenience; equivalent commands are shown in README)

.PHONY: install test bench lint

install:
	pip install -e ".[dev]"

test:
	pytest -q

# default baseline row
bench:
	python -m pibench.cli bench --stack none --model mock --suite injecagent-seed

lint:
	ruff check src tests
