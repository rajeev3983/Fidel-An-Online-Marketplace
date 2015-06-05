Fidel
====================================================
Fidel is an online marketplace for selling or buying second hand items within your friend circle. This project is part of database project.

**Instructions to install django**
_____________________________________________________

- Download the latest django release from https://www.djangoproject.com/download/ . We will be working with django-1.7.
- Extract the tar and cd into the extracted directory.
- Use command "sudo python setup.py install" to install django
- Use command  python -c "import django; print django.VERSION" to check your django version. You will get an error message if django is not installed properly.

**Instructions to set up database**
_______________________________________________________
- Install postgresql on your system.
- Install psycopg2 library from http://initd.org/psycopg/
- create a database named fidel_database
- create a database user with name fidel_user and password fidel_password
- clone the project from remote repository using command "git clone https://gitlab.com/ayushbgl/Fidel.git"
- Find manage.py file in Fidel/fidel and run command "python manage.py migrate". You should see something like this if the database connection is successful


**Instructions to set up tables and populate them**
_______________________________________________________________
- Clone the project using 'https://gitlab.com/ayushbgl/Fidel.git'
- cd into the folder containing manage.py
- Use command 'python manage.py makemigrations' to make migrations
- Use command 'python manage.py migrate' to make tables for your database
- Use command 'python manage.py shell &lt;dummy_database.txt' to populate the database
 
-Note: Some of the database tables(message, notifications ) have not been been populated yet. Will populate then later. For now it should be enough to get started. Also domain value is random string for now. Will correct it later.


**Some useful links/ commands**
__________________________________________________________
*User login in postgres*

psql fidel_user  -h 127.0.0.1 -d fidel_database

*Some useful postgresql commands*

- postgres=# \h                 &nbsp # help on SQL commands
- postgres=# \?                 # help on psql commands, such as \? and \h
- postgres=# \l                 # list databases
- postgres=# \c database_name   # connect to a database
- postgres=# \d                 # list of tables
- postgres=# \d table_name      # schema of a given table
- postgres=# \du                # list roles
- postgres=# \e                 # edit in $EDITOR

*drop all tables from database*
select 'drop table if exists "' || tablename || '" cascade;' 
  from pg_tables
 where schemaname = 'public';