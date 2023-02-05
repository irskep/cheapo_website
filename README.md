# Cheapo Website Boilerplate

Hosting web sites with databases is too damn expensive if you follow the instructions on Render, Digital Ocean, Heroku, etc. They all suggest you connect a \$15+/month managed database to your rinky-dink Python app, and you end up paying like $25/month and still having strict limitations. Meanwhile, many people claim SQLite is a perfectly good production database for small web sites, but nobody tells you how to actually deploy it with persistent storage.

Well, I figured it out. Here it is. Fork this repo, change the service name in `render.yaml`, modify the code to your heart's content, and deploy it to [render.com](https://render.com) for $8/mo. Or you can deploy to [Fly.io](https://fly.io) on the free tier, capped at $2/mo if you exceed it.

**This setup does not do zero-downtime deployments. Your web site will go down for about a minute during each deploy. 😱‼️**

**Although I've done my best to test this code and these instructions, it's still just a small weekend experiment, so there might be mistakes.**

It's 95% Flask boilerplate.

Features:

- Basic Flask setup with blueprints
- Flask-Login, Flask-SQLAlchemy, and Flask-Migrate are already configured
- Basic login/register/logout functionality
- Maintenance mode for running database migrations

## Development

Common workflows are written as Make commands. These docs assume you're using macOS, but everything should translate to Linux other than some installation steps.

### 1. Set up Poetry

Python dependencies are managed using [Poetry](https://python-poetry.org) in development, and using Pip in production.

```sh
poetry init
poetry install
```

### 2. Run migrations

Migrations are always applied on the command line, never automatically.

```sh
make local-runmigrations
```

### 2. Run the local development server

```
make serve
```

## Deployment with Render

### First-time setup

1. Use Render's [Blueprints](https://dashboard.render.com/blueprints) feature.
2. Set some environment variables on the dashboard for your new web service:
   - `FLASK_SECRET_KEY`: a random string (https://www.uuidgenerator.net).
   - `FLASK_MAINTENANCE_MODE`: `1` (this will run your first deploy in maintenance mode so you can run migrations)
3. Use Render's in-browser SSH page to log in and run `make maintenance-runmigrations`.
4. Set `FLASK_MAINTENANCE_MODE` to `0`, and Render will redeploy the site. You should now be able to use the database.

### Database migrations

Familiarize yourself with [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/). Unfortunately for all us web backend developers, we can never escape database migrations, and we need to do them right.

Whenever you make a change to your database, follow these steps:

1. Make the change in your Python source code. Consider using [deferred column loading](https://docs.sqlalchemy.org/en/14/orm/loading_columns.html#deferred-column-loading) to eliminate runtime errors before your migration has been applied to your database.
2. Run `make local-db-migrate` (alias for `poetry run flask --app server db migrate`) to create the migration files. Check them by hand.
3. Run `make local-db-upgrade` (alias for `poetry run flask --app server db upgrade`)
4. Commit your changes.
5. Set the web site to maintenance mode (`FLASK_MAINTENANCE_MODE=1`).
6. Deploy your changes.
7. SSH into your service.
8. Run `make maintenance-db-upgrade`.
9. Set the web site back to normal mode (`FLASK_MAINTENANCE_MODE=0`).
10. If you used deferred column loading, you can now remove the `deferred()` wrappers.

## Deployment with Fly.io

### First-time setup

1. In `fly.toml`, set `FLASK_MAINTENANCE_MODE` to `1` (instead of `0`) so your first deploy runs in maintenance mode.
2. Run `fly deploy` to create and deploy an app. (You might need to use `fly launch` instead, I forget. Someone please send me a PR to update this sentence.)
3. Run `fly secrets set FLASK_SECRET_KEY=(random string)` (https://uuidgenerator.net).
4. Run `fly ssh console`. In the SSH session, `cd /code && make maintenance-db-upgrade`. (It should be possible to get this down to one line, but I'm having trouble with `fly ssh console -C`.)
5. In `fly.toml`, set `FLASK_MAINTENANCE_MODE` back to `0`.
6. Run `fly deploy` to redeploy the site without maintenance mode.

### Database migrations

Familiarize yourself with [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/). Unfortunately for all us web backend developers, we can never escape database migrations, and we need to do them right.

Whenever you make a change to your database, follow these steps:

1. Make the change in your Python source code. Consider using [deferred column loading](https://docs.sqlalchemy.org/en/14/orm/loading_columns.html#deferred-column-loading) to eliminate runtime errors before your migration has been applied to your database.
2. Run `make local-db-migrate` (alias for `poetry run flask --app server db migrate`) to create the migration files. Check them by hand.
3. Run `make local-db-upgrade` (alias for `poetry run flask --app server db upgrade`)
4. Commit your changes.
5. Set the web site to maintenance mode (`fly secrets set FLASK_MAINTENANCE_MODE=1`).
6. Run `fly ssh console`. In the SSH session, `cd /code && make maintenance-db-upgrade`. (It should be possible to get this down to one line, but I'm having trouble with `fly ssh console -C`.)
7. Set the web site back to normal mode (`fly secrets set FLASK_MAINTENANCE_MODE=0`).
8. If you used deferred column loading, you can now remove the `deferred()` wrappers.

## Organization

All Python code is inside `server`, leaving you space to create a `client` directory for rich JS apps if you like.

All view functions are inside Flask Blueprints. Each blueprint is defined in a file with a `bp_` prefix. I like this prefix because it keeps the directory flat and makes imports look really obvious, but of course you can rename the files if you want.

`bp_maintenance.py` contains the routes for maintenance mode (every page will say "this web site is in maintenance mode"). You can remove this file and the call to it in `create_app.py` if you can handle the SQLite database being opened in read-only mode, which is probably nicer.

`inside` refers to the logged-in-user-oriented views (like "dashboard"), and `outside` refers to logged-out-user-oriented views (like "index", the landing page).

## Backups???

Render automatically backs up the disk every day, so you have data from at most 24 hours ago.
