# migration to ubuntu server

    sudo apt-get install -y postgresql
    sudo su - postgres
    createuser --createdb --username postgres --no-createrole --superuser --pwprompt postgresuser
    createdb database_name

# go to project 

    cd project
    python manage.py makemigrations
    python manage.py migrate
    
