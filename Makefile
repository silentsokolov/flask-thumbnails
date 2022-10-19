.PHONY: check-black check-isort check-pylint static-analysis test sdist wheel release pre-release clean

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal

release: clean sdist wheel
	twine upload dist/*

pre-release: sdist wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$)' | xargs rm -rf
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

check-black:
	@echo "--> Running black checks"
	@black --check --diff .

check-isort:
	@echo "--> Running isort checks"
	@isort --check-only .

check-pylint:
	@echo "--> Running pylint checks"
	@pylint `git ls-files '*.py'`

check-yamllint:
	@echo "--> Running yamllint checks"
	@yamllint .

lint: check-black check-isort check-pylint check-yamllint

# Format code
.PHONY: fmt

fmt:
	@echo "--> Running isort"
	@isort .
	@echo "--> Running black"
	@black .

# Test
.PHONY: test

test:
	@echo "--> Running tests"
	PYTHONPATH=".:tests:${PYTHONPATH}" python setup.py test

coverage:
	@echo "--> Running coverage"
	PYTHONPATH=".:tests:${PYTHONPATH}" coverage run --omit='setup.py' --omit='tests/*' --source='.' setup.py test
