rm -f db.sqlite3

rm -rf dashboard/__pycache__
rm -rf dashboard/migrations
mkdir dashboard/migrations
touch dashboard/migrations/__init__.py 

rm -rf account/__pycache__
rm -rf account/migrations
mkdir account/migrations
touch account/migrations/__init__.py 

rm -rf accreditation/__pycache__
rm -rf accreditation/migrations
mkdir accreditation/migrations
touch accreditation/migrations/__init__.py 

python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py createsuperuser
python3 manage.py collectstatic
python3 populate.py
