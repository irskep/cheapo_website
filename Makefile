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

### fly.io stuff (delete if you use render) ###

fly-makevolume:
# change 'cheapo' to your app name
# change 'sjc' to your region
	fly volumes create -a cheapo -r sjc --size 1 data