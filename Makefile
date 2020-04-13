prepare:
	python3 manage.py makemigrations

setup:
	pipenv install
	pipenv run python3 manage.py migrate

start-server:
	pipenv run python3 manage.py runserver

start-background-server:
	pipenv make start-server &

start-workers:
	pipenv run python3 manage.py workers

start-background-workers:
	nohup make start-workers &

create-super-user:
	pipenv run python3 manage.py createsuperuser