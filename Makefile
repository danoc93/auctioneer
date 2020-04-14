prepare:
	python3 manage.py makemigrations
	pipenv lock

setup:
	pipenv install
	pipenv run python3 manage.py migrate
	sh scripts/build_crons.sh | crontab -

start-server:
	pipenv run python3 manage.py runserver

start-background-server:
	nohup make start-server > /tmp/logs/auctioneer_server.out 2>&1 &

create-super-user:
	pipenv run python3 manage.py createsuperuser