PYTHON=.venv/bin/python # path to pyphon
PIP=.venv/bin/pip # path to pip
SOURCE_VENV=. .venv/bin/activate # source venv

install:
	$(PYTHON) -m venv .venv
	$(SOURCE_VENV) && $(PIP) install -r ./opply_project/requirements.txt

freeze:
	$(SOURCE_VENV) && $(PIP) freeze > ./opply_project/requirements.txt

shell:
	$(SOURCE_VENV) && $(PYTHON) ./opply_project/manage.py shell

create-superuser:
	$(SOURCE_VENV) && $(PYTHON) ./opply_project/manage.py createsuperuser

run-server:
	$(SOURCE_VENV) && $(PYTHON) ./opply_project/manage.py runserver

run-docker:
	docker-compose up --build

test:
	$(SOURCE_VENV) && $(PYTHON) ./opply_project/manage.py test api.identity api.catalog api.orders

test-watch:
	ptw --config ./opply_project/pytest.ini

check-deploy:
	$(SOURCE_VENV) && $(PYTHON) ./opply_project/manage.py check --deploy