#!/bin/sh

echo "Running Database Migrations"
python manage.py makemigrations
python manage.py migrate

echo "Seed the database with initial data"
python manage.py loaddata ./api/identity/fixtures/Users.json --format=json --database=default
python manage.py loaddata ./api/identity/fixtures/Customers.json --format=json --database=default
python manage.py loaddata ./api/catalog/fixtures/Products.json --app catalog.Product --format=json --database=default
python manage.py loaddata ./api/catalog/fixtures/Inventory.json --app catalog.Inventory --format=json --database=default

exec "$@"