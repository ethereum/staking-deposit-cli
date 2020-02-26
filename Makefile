clean:
	rm -rf eth2.0-specs/
	rm -rf venv/
	find . -name __pycache__ -exec rm -rf {} \;
	find . -name .mypy_cache -exec rm -rf {} \;
	find . -name .pytest_cache -exec rm -rf {} \;

install_test:
	python3 -m venv venv; . venv/bin/activate; pip3 install -r requirements.txt

test: 
	. venv/bin/activate; cd ./src; python -m pytest

lint:
	. venv/bin/activate; flake8 --ignore=E252,W504,W503 --max-line-length=120 ./src/ && mypy --follow-imports=skip --ignore-missing-imports ./src/
