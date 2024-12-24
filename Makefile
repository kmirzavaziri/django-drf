.PHONY: test-deps
test-deps:
	pip install -r requirements/python/test.txt

.PHONY: dev-deps
dev-deps:
	pip install -r requirements/python/dev.txt

.PHONY: lint
lint: test-deps
	flake8 .
	black --check .
	isort --check-only .
	mypy .

.PHONY: format
format: test-deps
	black .
	isort .

.PHONY: pre-commit-install
pre-commit-install: dev-deps
	pre-commit install

.PHONY: test
test: test-deps
	python manage.py test polls
