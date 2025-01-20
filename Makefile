

run:
	venv/bin/flask --app ar_server --debug run --host 0.0.0.0 --port 5000  --cert adhoc --reload

venv:
	python -m venv venv
	venv/bin/pip install pyopenssl
	venv/bin/pip install -e .

init:
	venv/bin/flask --app ar_server --debug init-db

install: venv init

explore_db:
	sqlite3 instance/ar_db.sqlite

uninstall:
	rm -rf venv

reinstall: uninstall install