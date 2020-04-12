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

## Adding npm packages
    # Navigate back to root dir
    cd ..

    # Install axios
    docker-compose run --rm frontend npm add axios

    # Stop services
    docker-compose down

    # Rebuild
    docker-compose up --build

## Adding django apps
    # Navigate back to root dir
    cd ..
    
    docker-compose run --rm backend python3 manage.py startapp nameOfApp


