# TechGenies Intranet/Hub Web Application
### April 12th, 2020 - Dylan Gonzales (Full-Stack Developer)

This is the start of my README.md for the internal TechGenies Intranet/Hub Web Application.

Presumably, this will be adapted and changed overtime; I'll just be listing my thoughts, plans, and 
architectural designs for the time being.

## Dependencies

- Requires [Docker](https://docs.docker.com/docker-for-mac/install/)

## Stack Description
- **Django** v2.2
- **React JS** v13.10
- **npm** v6.13.7
- **sqlite** default w/ django (maybe use MySQL for prod?)

## Setup from git clone
In your terminal, run:
    
    git clone https://github.com/dgonzo27/react-django-docker-boiler.git
    
Build and Run the app:

    # Navigate into directory
    cd react-django-docker-boiler
    
    # Build and Run
    docker-compose up
    
Results seen at http://localhost:3000

## Deploy as a production app

### Steps for Success
1. Set up Django to use WhiteNoise for serving static files in production
2. Create a production Dockerfile that combines the frontend and backend services into a single app
3. Create a new AWS app to deploy to? Heroku?
4. Configure app to deploy a Docker image to AWS ECR

### 1. Set up Django to use WhiteNoise for prod
Create a settings file for each environment, all of which inherit from some base settings, then determine which settings file to use with an environment variable.  

In `backend/genie_hub`, create a settings folder with __init__.py inside:

    cd backend
    cd genie_hub
    mkdir settings
    cd settings
    TOUCH __init__.py

Move the existing `settings.py` file into it and rename it `base.py`.  

To make sure I don't accidentally deploy with unsafe settings, cut the following code from `base.py`, and paste it into a newly-created `development.py`:

    # Quick-start development settings -unsuitable for production
    # See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "blah blah blah"

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ["backend"]

At the top of the development.py file, add the line:

    genie_hub.settings.base import * 

Update `BASE_DIR` in `base.py` to point to the correct directory, which is now one level higher:

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

Update default in `backend/genie_hub/wsgi.py` to `genie_hub.settings.base` and add the following to the `backend` service in `docker-compose.yml`:

    environment:
      - DJANGO_SETTINGS_MODULE=genie_hub.settings.development

Create production.py settings in settings directory:

    import os
    from genie_hub.settings.base import *

    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False
    ALLOWED_HOSTS = [os.environ.get("PRODUCTION_HOST")]

The `SECRET_KEY` should be some long string of random characters (last pass generated) and save it as an environment/config variable away from source control

To enable WhiteNoise to serve frontend assets, add the following to production.py:

    INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

    # Must insert after SecurityMiddleware, which is first in settings/common.py
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    TEMPLATES[0]["DIRS"] = [os.path.join(BASE_DIR, "../", "frontend", "build")]

    STATICFILES_DIRS = [os.path.join(BASE_DIR, "../", "frontend", "build", "static")]
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    STATIC_URL = "/static/"
    WHITENOISE_ROOT = os.path.join(BASE_DIR, "../", "frontend", "build", "root")

* `TEMPLATES`: directories with templates or html files
* `STATICFILES_DIRS`: directory where Django can find html, js, css, and other static assets
* `STATIC_ROOT`: directory to which Django will move the static assets and from which it will serve them when the app is running
* `WHITENOISE_ROOT`: directory where WhiteNoise can find all **non-html** static assets

Make Django aware of the path `/`, because right now it only knows about `/admin` and `/char_count`. 

Update `/backend/genie_hub/urls.py` to look like the following:

    from django.contrib import admin
    from django.urls import path, re_path
    from django.views.generic import TemplateView
    from char_count.views import char_count

    urlpatterns = [
      path("admin/", admin.site.urls),
      path("char_count", char_count, name="char_count"),
      re_path(".*", TemplateView.as_view(template_name="index.html")),
    ]

Adding `.*` to the regex path tells Django to respond to any request that don't contain explicit instructions by sending the user `index.html`.  In a dev env, React's Webpack server will still handle calls to `/` (and any path other than the two defined above), but in prod, when there's no Webpack server, Django will serve `index.html` from the static files directory.  Using `.*` instead of a specific path gives the freedom to define as many paths as we want for the frontend to handle (with React Router for example) without having to update Django's URLs list.

Create production Dockerfile:

    FROM python:3.7

    # Install curl, node and yarn
    RUN apt-get -y install curl \
      && curl -sL https://deb.nodesource.com/setup_13.10 | bash \
      && apt-get install nodejs
      && curl -o- -L https://yarnpkg.com/install.sh | bash

    WORKDIR /app/backend

    # Install Python dependencies
    COPY ./backend/requirements.txt /app/backend/
    RUN pip3 install --upgrade pip -r requirements.txt

    # Install JS dependencies
    WORKDIR /app/frontend

    COPY ./frontend/package.json ./frontend/yarn.lock /app/frontend/
    RUN $HOME/ .yarn/bin/yarn install

    # Add the rest of the code
    COPY ./app/

    # Build static files
    RUN $HOME/ .yarn/bin/yarn build

    # Have to move all static files other than index.html to root/ for whitenoise middleware
    WORKDIR /app/frontend/build

    RUN mkdir root && mv *.ico *.js *.json root

    # Collect static files
    RUN mkdir /app/backend/staticfiles

    WORKDIR /app

    # SECRET_KEY is only included here to avoid raising an error when generating static files
    RUN DJANGO_SETTINGS_MODULE=genie_hub.settings.production \
    SECRET_KEY=somethingsupersecret \
    python3 backend/manage.py collectstatic --noinput


    EXPOSE $PORT

    CMD python3 backend/manage.py runserver 0.0.0.0:$PORT


