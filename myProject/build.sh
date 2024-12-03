pip install -r requirements.txt
python manage.py migrate  # Apply migrations
python manage.py collectstatic --noinput  # Collect static files
