### commands to run while in maintenance mode ###

maintenance-db-upgrade:
	export FLASK_MAINTENANCE_MODE = 0
	flask --app server db upgrade

### commands to run locally ###

local-serve:
	poetry run python -m flask --app server --debug run

local-db-migrate:
	poetry run python -m flask --app server db migrate

local-db-upgrade:
	poetry run python -m flask --app server db upgrade

# you need to run this in order for prod to install the same dependencies you have in Poetry
local-freeze-deps:
	rm -f requirements.txt
	poetry export --without-hashes > requirements.txt

### fly.io stuff (delete if you use render) ###

fly-makevolume:
# change 'cheapo' to your app name
# change 'sjc' to your region
	fly volumes create -a cheapo -r sjc --size 1 data