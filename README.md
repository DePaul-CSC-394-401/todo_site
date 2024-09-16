Docker initial setup:
1. docker compose up 
2. **In new terminal:** docker compose exec web python manage.py migrate
3. **Run on initial setup only:** docker compose exec web python manage.py createsuperuser --noinput

Virtual environment setup:

1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt

After making changes to project:
1. python manage.py makemigrations
2. docker compose up
3. docker compose exec web python manage.py migrate
