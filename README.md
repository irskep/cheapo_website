# Cheapo Website Boilerplate

Hosting web sites with databases is too damn expensive if you follow the instructions on Render, Digital Ocean, Heroku, etc. They all suggest you connect a $15+/mo managed database to your rinky-dink Python app. Meanwhile, many people claim SQLite is a perfectly good production database for small web sites, but nobody tells you how to actually deploy it with persistent storage.

Well, I figured it out. Here it is. Fork this repo, change the service name in `render.yaml`, and modify the code to your heart's content.

It's 95% Flask boilerplate.

Features:

- Basic Flask setup with blueprints
- Flask-Login and Flask-SQLAlchemy are already configured
- Basic login/register/logout functionality

## Development

```sh
poetry init
poetry install
make serve
```

## Deployment

1. Use Render's [Blueprints](https://dashboard.render.com/blueprints) feature.
2. Set the `FLASK_SECRET_KEY` env var to be a random string (https://www.uuidgenerator.net).

## Cost

Less than $10/mo using the default settings on the `starter` plan, depending on disk usage.

## Organization

All Python code is inside `server`, leaving you space to create a `client` directory for rich JS apps if you like.

All view functions are inside Flask Blueprints. Each blueprint is defined in a file with a `bp_` prefix. I like this prefix because it keeps the directory flat and makes imports look really obvious, but of course you can rename the files if you want.

`inside` refers to the logged-in-user-oriented views (like "dashboard"), and `outside` refers to logged-out-user-oriented views (like "index", the landing page).

## Backups???

Render automatically backs up the disk every day, so you have data from at most 24 hours ago.
