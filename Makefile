build:
	python setup.py sdist

register:
	python setup.py register

upload:
	python setup.py bdist_wheel upload

install:
	python setup.py install

clean:
	@rm -rf .Python MANIFEST build dist venv* *.egg-info *.egg
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

.PHONY: build register upload clean install