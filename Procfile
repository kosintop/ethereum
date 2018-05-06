web: env PYTHONPATH=$PYTHONPATH:$PWD/eth gunicorn eth.eth.wsgi:application
release: python manage.py migrate