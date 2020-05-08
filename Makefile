VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3.8

help:
	@echo "clean - remove build and Python file artifacts"
	@echo "deposit - run deposit-cli"
	@echo "build - install basic dependencies"
	@echo "build_test - install testing dependencies"
	@echo "lint - check style with flake8 and mypy"
	@echo "test - run tests"

clean:
	rm -rf venv/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name __pycache__ -exec rm -rf {} \;
	find . -name .mypy_cache -exec rm -rf {} \;
	find . -name .pytest_cache -exec rm -rf {} \;

$(VENV_NAME)/bin/activate: requirements.txt
	@test -d $(VENV_NAME) || python3 -m venv --clear $(VENV_NAME)
	${VENV_NAME}/bin/python -m pip install -r requirements.txt
	${VENV_NAME}/bin/python -m pip install -r requirements_test.txt
	@touch $(VENV_NAME)/bin/activate

build: $(VENV_NAME)/bin/activate

build_test: build
	${VENV_NAME}/bin/python -m pip install -r requirements_test.txt

test: build_test
	$(VENV_ACTIVATE) && python -m pytest .

lint: build_test
	$(VENV_ACTIVATE) && flake8 --config=flake8.ini ./eth2deposit ./cli ./tests && mypy --config-file mypy.ini -p eth2deposit -p tests -p cli

deposit: build
	$(VENV_ACTIVATE) && python setup.py install; python ./cli/deposit.py
