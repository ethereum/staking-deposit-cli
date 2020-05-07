clean:
	rm -rf venv/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name __pycache__ -exec rm -rf {} \;
	find . -name .mypy_cache -exec rm -rf {} \;
	find . -name .pytest_cache -exec rm -rf {} \;

install:
	python3 -m venv venv; . venv/bin/activate; pip3 install -r requirements.txt

install_test:
	python3 -m venv venv; . venv/bin/activate; pip3 install -r requirements_test.txt

test: 
	. venv/bin/activate; cd src; python -m pytest .

lint:
	. venv/bin/activate; flake8 --ignore=E252,W504,W503 --max-line-length=120 ./src/ \
	&& mypy --follow-imports=skip --ignore-missing-imports -p src
