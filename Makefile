serve:
	poetry run python -m flask --app server --debug run

initdb:
	poetry run python -m flask --app server initdb

resetdb:
	rm -f instance/project.db
	poetry run python -m flask --app server initdb