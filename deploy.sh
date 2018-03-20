export FLASK_APP=autoapp.py
export FLASK_DEBUG=0
npm run-script build-colorless
npm run-script gunicorn-server
