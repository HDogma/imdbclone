# Delete database, migration directories
rm db.sqlite3
rm -rf main/migrations/0*

# Create migrations
python3 manage.py makemigrations
python3 manage.py makemigrations main

# Migrate
python3 manage.py migrate

# Create admin
python3 manage.py createsuperuser

