# migration to ubuntu server

    sudo apt-get install -y postgresql
    sudo su - postgres
    createuser --createdb --username postgres --no-createrole --superuser --pwprompt postgresuser
    createdb --owner=postuser users
    
# go to project 

    cd project
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip python3-venv -y
    python3 -m venv venv
    source venv/bin/activate
    pip install django djangorestframework
    django-admin startproject myproject
    django-admin startapp app

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

    python manage.py runserver 0.0.0.0:8080

