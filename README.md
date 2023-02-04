# Cheapo Website Boilerplate

Hosting web sites with databases is too damn expensive if you follow the instructions on Render, Digital Ocean, Heroku, etc. They all suggest you connect a \$15+/month managed database to your rinky-dink Python app, and you end up paying like $25/month and still having strict limitations. Meanwhile, many people claim SQLite is a perfectly good production database for small web sites, but nobody tells you how to actually deploy it with persistent storage.

Well, I figured it out. Here it is. Fork this repo, change the service name in `render.yaml`, modify the code to your heart's content, and deploy it to `render.com` for $8/mo.

(Also working on fly.io support, but it doesn't work yet.)

It's 95% Flask boilerplate.

Features:

- Basic Flask setup with blueprints
- Flask-Login and Flask-SQLAlchemy are already configured
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

1. Make the change in your Python source code.
2. Run `make local-db-upgrade` (alias for `poetry run flask --app server db upgrade`) to create the migration files. Check them by hand.
3. Run `make local-db-migrate` (alias for `poetry run flask --app server db migrate`)
4. Commit your changes.
5. Set the web site to maintenance mode (`FLASK_MAINTENANCE_MODE=1`).
6. Deploy your changes.
7. SSH into your service.
8. Run `make maintenance-db-migrate`.
9. Set the web site to normal mode (`FLASK_MAINTENANCE_MODE=0`).

## Organization

All Python code is inside `server`, leaving you space to create a `client` directory for rich JS apps if you like.

All view functions are inside Flask Blueprints. Each blueprint is defined in a file with a `bp_` prefix. I like this prefix because it keeps the directory flat and makes imports look really obvious, but of course you can rename the files if you want.

`inside` refers to the logged-in-user-oriented views (like "dashboard"), and `outside` refers to logged-out-user-oriented views (like "index", the landing page).

## Backups???

Render automatically backs up the disk every day, so you have data from at most 24 hours ago.
