# nnsave_backend

The backend for the NNSave app for the iNNovate hackathon

# Installation

## Packages

In the current state, this only runs on linux.
You need to have the following installed
(these are the debian package names):

 * python-dev
 * libpq-dev
 * postgresql-9.5
 * postgresql-contrib-9.5
 * postgresql-9.5-postgis-2.2
 * postgresql-9.5-postgis-scripts
 * postgis
 * binutils
 * libproj-dev
 * gdal-bin
 * python-gdal
 * python-pip

These package might not be entirely correct, and there might be some extra packages.

## VirtualEnv

You also need virtualenv, which can be installed through pip
```
sudo pip install virtualenv
```

You should be able to source the existing virtualenv in venv/bin/activate,
but if you need to recreate the venv, here is the packaged installed:
```
pip install django psycopg2 django-import-export
```

## Postgresql setup

You will need to setup a postgres database with a user and a few options set.
The database needs the postgis extension loaded.
Here is what I ran to create the database:
```shell
sudo su - postgres
psql
```
```SQL
CREATE DATABASE nnsave;
CREATE USER nnsave_user WITH PASSWORD 'nnsave_password';
ALTER ROLE nnsave_user SUPERUSER;
ALTER ROLE nnsave_user SET client_encoding TO 'utf8';
ALTER ROLE nnsave_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE nnsave_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE nnsave TO nnsave_user;
\q
```
```shell
psql nnsave -c 'CREATE EXTENSION postgis'
exit
```

## Migrations

When first installing the server, the migrations must be applied to the database.
```shell
python manage.py migrate
```

# Usage

To run the development server, source the virtual enviornment, then run the django dev server
```shell
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

# Importing from CSV

One thing I had to do was import a list of discount locations, I did this
by saving a spreadsheet as a csv. The first row of the csv should be the
column headers. There should be a column for every field on the object.
I ran `python manage.py shell` to enter the django shell then ran the following
python code. This is written from memory and might not be correct. This code
assumes that every row has at least a valid name, description, latitude and longitude
```python
import csv
from nnsave_app.models import Location, Category
from django.contrib.gis.geos import Point
myfile = open('path/to/import.csv', 'r+b')
mycsv = csv.DictReader(myfile)
for row in mycsv:
     pnt = Point(row['Latitude'],row['Longitude'])
     cat, created = Category.objects.get_or_create(row['Category'].strip())
     loc, created = Location.objects.get_or_create(name=row['Name'].strip(),
                          phone=row['Phone'].strip(),
                          website=row['Website'].strip(),
                          email=row['Email'].strip(),
                          address=row['Address'].strip(),
                          loc=pnt,
                          description=row['Description'].strip(),
                          category=cat)
```

I had hoped to get Django import_export to work with this importing, but I couldn't figure out how to get Points with it.
Maybe in the future. If import_export gets working it could be added to the admin interface to make it super simple to import locations

# Hackathon

If you are interestedin what code was written in the hackathon,
everything up to commit c2c780e was done at the hackathon
