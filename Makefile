serve:
	poetry run python -m flask --app server --debug run

initdb:
	poetry run python -m flask --app server initdb

resetdb:
	rm -f instance/project.db
	poetry run python -m flask --app server initdb

freeze-deps:
	rm -f requirements.txt
	poetry export --without-hashes > requirements.txt

docker-build:
	docker build -t cheapo .

docker-run:
#	run 'cheapo', map port 5000, and stay attached to STDIN/STDOUT/STDERR
	docker run -d cheapo -p 5000:5000 -a

fly-makevolume:
# change 'cheapo' to your app name
# change 'sjc' to your region
	fly volumes create -a cheapo -r sjc --size 1 litefs