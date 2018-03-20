export FLASK_APP=autoapp.py
export FLASK_DEBUG=0
npm run build
gunicorn twitter_python_mentors.app:create_app() -b 0.0.0.0:$PORT -w 3
