python -m venv venv

venv/pip/install -e .


export FLASK_APP=ar_server; 
export FLASK_ENV=development; 
venv/bin/flask init-db;



venv/bin/flask run