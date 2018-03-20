export FLASK_APP=autoapp.py
export FLASK_DEBUG=0
npm run-script build-colorless
flask db init
flask db migrate
flask db upgrade
npm run-script gunicorn-server
