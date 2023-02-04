### commands to run while in maintenance mode ###

maintenance-runmigrations:
	export FLASK_MAINTENANCE_MODE = 0
	flask --app server:app db migrate

### commands to run locally ###

local-serve:
	poetry run python -m flask --app server --debug run

local-initdb:
	poetry run python -m flask --app server initdb

local-resetdb:
	rm -f instance/project.db
	poetry run python -m flask --app server initdb

# you need to run this in order for prod to install the same dependencies you have in Poetry
local-freeze-deps:
	rm -f requirements.txt
	poetry export --without-hashes > requirements.txt

### fly.io stuff (delete if you use render) ###

fly-makevolume:
# change 'cheapo' to your app name
# change 'sjc' to your region
	fly volumes create -a cheapo -r sjc --size 1 data