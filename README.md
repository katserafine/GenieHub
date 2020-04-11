# Docker + Django + React App Boiler Plate

Code repo for my ideal integration of Django and React - set up with Docker Compose

## Dependencies

- Requires [Docker](https://docs.docker.com/docker-for-mac/install/)

## Stack Description
- **Django** v2.2
- **React JS** v13.10
- **npm** v6.13.7
- **sqlite** default w/ django (maybe use MySQL for prod?)

## Setting up the app

* I want to start out with a clear separation between the frontend and backend
* I want to focus on server-side logic to ensure this app and CRUD API can be scalable for B2B products
* With my development experience inheriting Genetics Maven, static javascript assets are being used in Django views and I cannot use hot-reloading
* ^ That means I have to run my build script `npm run build-development` that takes 1-2 minutes for the webpack to recompile everytime I change any react code - SUPER FRUSTRATING FOR INEXPERIENCED REACT DEVS!

## Historical Setup from Scratch
This is just to provide an understanding of how this repo got to where it is.  Don't do this if you're cloning the repo, but this should work if you want to build your own locally on your machine from scratch.

### Steps for Success
1. Create django web-app that runs in Docker container
2. Create React app that runs in Docker container
3. Run the two containers in parallel as services with docker-compose
4. Connect frontend proxy to backend host (serve backend API)

### 1. Create django web-app
Navigate to clean/desired app directory.  Make directory for app, and backend dir within app dir:

    mkdir AppName
    cd AppName
    mkdir backend
    cd backend

Make requirements.txt for backend dir (django only or add DRF if you know you'll use it later)

    vim requirements.txt

    django

Add Dockerfile in backend directory:

    # Use an official Python runtime as a parent image
    FROM python:3.7

    # Adding backend directory to make absolute filepaths consistent across services
    WORKDIR /app/backend

    # Install Python dependencies
    COPY requirements.txt /app/backend
    RUN pip3 install --upgrade pip -r requirements.txt

    # Add the rest of the code
    COPY . /app/backend

    # Make port 8000 available for the app
    EXPOSE 8000

    CMD python3 manage.py runserver 0.0.0.0:8000

From terminal, navigate up a directory:

    cd ..

Build image:

    docker build -t [DockerHubUsernameIfYouWant/]backend:latest backend

Create django project command at `.` directory:

    docker run -v $PWD/backend:/app/backend backend:latest django-admin startproject genie_hub .

Run image at port 8000:8000:

    docker run -v $PWD/backend:/app/backend -p 8000:8000 backend:latest

The app should be up and running on http://localhost:8000.  To stop the app, `CMD + t` for a new terminal tab, `docker ps` to see running containers, copy ID and run:

    docker stop [containerID]

### 2. Create react web-app
Similar to backend, make frontend directory:

    ls
    # should list your backend directory
    mkdir frontend
    cd frontend

Create a Dockerfile with some lines commented out since the files don't exist yet:

    # Use an official node runtime as a parent image
    FROM node:13.12.0

    WORKDIR /app/

    # Install dependencies
    # COPY package.json yarn.lock /app/

    # RUN npm install

    # Add rest of the client code
    COPY ./app/

    EXPOSE 3000

    # CMD npm start

Change back to root directory:

    cd ..

Build image:

    docker build -t [DockerHubUsernameIfYouWant/]frontend:latest frontend

Create React App command:

    docker run -v $PWD/frontend:/app frontend:latest npx create-react-app genie-den

Move content in local /genie-den react dir to container dir, add frontend dir to .gitignore and local directory for genie-den:

    mv frontend/genie-den/* frontend/genie-den/ .gitignore frontend/ && rmdir frontend/genie-den

Run image at port 3000:3000

    docker run -v $PWD/frontend:app -p 3000:3000 frontend:latest npm start

Make sure the app is running on http://localhost:3000

Go back to the Dockerfile in /frontend and uncomment any commented lines so that the next build will include all the commands

### 3. Set up docker-compose services for frontend and backend
In root directory, add docker-compose.yml file:

    version: "3"
    services:
    	backend:
    		build: ./backend
		volumes:
			- ./backend:/app/backend
		ports:
			- "8000:8000"
		stdin_open: true
		tty: true
		command: python3 manage.py runserver 0.0.0.0:8000
	frontend:
		build: ./frontend
		volumes: 
			- ./frontend:/app
			- /app/node_modules
		ports:
			- "3000:3000"
		environment:
			- NODE_ENV=development
		depends_on:
			- backend
		command: npm start

From root directory, running `docker-compose up` should build and start both services in parallel - http://localhost:8000 and http://localhost:3000

### 4. Connect Django and React
In a tutorial I found online, a simple JsonResponse with Django returns a given character count for a user entered string.  The frontend then displays the number of characters.  This is a base example for how the API will communicate to with React using the 
npm package `axios`.  

Here is how that was configured...

Create a _django app_ inside the django project (from root directory, not backend):

    docker-compose run --rm backend python3 manage.py startapp char_count

Create API response in new django app:

    cd backend/char_count/
    vim views.py

    from django.http import JsonResponse

    def char_count(request):
      '''
      Return the character count for a given text string
      '''
      
      text = request.GET.get("text", "")
      return JsonResponse({"count": len(text)})

Add new django app to _INSTALLED_APP_ section of the django project settings.py:

    cd ..
    cd genie_hub
    vim settings.py

    INSTALLED_APPS = [
        'char_count.apps.CharCountConfig',
    ]

    OR

    INSTALLED_APPS = [
        'char_count',
    ]

Add url pattern for _char_count_ to django project urls.py:

    vim urls.py

    from django.contrib import admin
    from django.urls import path
    from char_count.views import char_count

    urlpatterns = [
      path('admin/', admin.site.urls),
      path('char_count', char_count, name='char_count'),
    ]

Running the app and going to localhost:8000/characters?text=hello world should return a json count of 11

Update configs in backend and frontend to handle networking errors:

    vim settings.py

    ALLOWED_HOSTS = ["backend"]

    cd ..
    cd ..
    cd frontend
    vim package.json

    # End of file
      },
      "proxy": "http://backend:8000"
    }

Install npm package for `axios`:

    # Navigate back to root dir
    cd ..
    
    # Install axios
    docker-compose run --rm frontend npm add axios

    # Stop services
    docker-compose down

    # Rebuild
    docker-compose up --build

Add some js to App.js:

    # Navigate to App.js
    cd frontend
    cd src
    vim App.js

    # Full code:
    import React from 'react';
    import axios from 'axios';
    import './App.css'

    function handleSubmit(event) {
        const text = document.querySelector('#char-input').value

        axios
          .get(`/char_count?text=${text}`).then(({data}) => {
              document.querySelector('#char-count').textContent = `${data.count} characters!`
          })
          .catch(err => console.log(err))
    }

    function App() {
        return (
          <div className="App">
            <div>
              <label htmlFor='char-input'>How many characters does</label>
              <input id='char-input' type='text />
              <button onClick={handleSubmit}>have?</button>
            </div>
            <div>
              <h3 id='char-count'></h3>
            </div>
          </div>
        );
    }

    export default App;

Save, back to root directory and run it:

    cd ..
    cd ..
    docker-compose up

Go to http://localhost:3000 and boom.

If you're comfortable with Django and React it should be pretty clear how to take it from here.