run-tests:
	@echo "Changed files: $(shell git diff --name-only --relative)"
	uv run scripts/graph_analyzer.py src/tests $(shell git diff --name-only --relative) | xargs uv run python -m unittest