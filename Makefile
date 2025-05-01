.PHONY: install lint test run

install:
	pip install -r requirements.txt

lint:
	flake8 . --max-line-length=120 --ignore=E501,E203,W503,F841,E722,E402,W605,W601,W601,E501,W291

run:
	streamlit run main.py
