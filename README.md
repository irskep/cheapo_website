# Cheapo Website Boilerplate

Hosting web sites with databases is too damn expensive if you follow the instructions on Render, Digital Ocean, Heroku, etc. They all suggest you connect a $15+/mo managed database to your rinky-dink Python app. Meanwhile, many people claim SQLite is a perfectly good production database for small web sites, but nobody tells you how to actually deploy it with persistent storage.

Well, I figured it out. Here it is. Fork this repo, change the service name in `render.yaml`, and modify the code to your heart's content.

Features:

- Basic Flask setup with blueprints
- Flask-Login and Flask-SQLAlchemy are already configured
- Basic login/register/logout functionality

## Deployment

1. Use Render's [Blueprints](https://dashboard.render.com/blueprints) feature.
2. Configure SECRET_KEY to be a random string (https://www.uuidgenerator.net).

## Cost

Less than $10/mo using the default settings.
