
rm: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -type d -iname '*egg-info' -exec rm -rdf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	# rm -rf .py.egg-info
	rm -rf .pytest_cache
	rm -rf .hypothesis
	rm -rdf assets
	

test: rm
	pytest -s -v  tests/

coverage-html:
	# --cov where you want to cover
	#  tests  where your test code is 
	pytest --cov=md_wash/ --cov-report=html tests/
	open htmlcov/index.html

coverage:
	pytest --cov=md_wash/ tests/


install: uninstall
	pip3 install . 

uninstall:
	pip3 uninstall  -y md_wash

main:
	python3 main.py eat -c 2

run:
	python3 -m md_wash  -c  -r  ~/bdcloud/notes/golang_最佳实践.md -o ./out


wrun:
	watchexec -ce py 'python3 -m md_wash ./notes -o ./notes2 -c \
	&& ls ./notes2/assets | wc -l \
	&& rm -rdf notes2'

wrunfile:
	watchexec -ce py 'python3 -m md_wash ./notes/python-爬虫笔记-简易.md  -c \
	&& ls ./notes2/assets | wc -l \
	&& rm -rdf notes2'

open:
	open ./notes/python-爬虫笔记-简易.md


all: rm uninstall install run 


pure-all: env-rm rm env install test run


	
upload-to-test: rm freeze
	python3 setup.py bdist_wheel --universal
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upload-to-prod: rm freeze
	python3 setup.py bdist_wheel --universal
	twine upload dist/*


freeze:
	# pipreqs will find the module the project really depneds
	pipreqs . --force

freeze-global:
	#  pip3 will find all the module not belong to standard  library
	pip3 freeze > requirements.txt


env-rm:
	rm -rdf env

env-create: 
	python3 -m venv env

env: env-create
	pip3 install -r requirements.txt

source: 
	echo "you need to manully source it"
	echo ". env/bin/activate"
	. env/bin/activate

auto_version:
	python version.py
