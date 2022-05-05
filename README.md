# Create a virtual environment to isolate our package dependencies locally
> `python3 -m venv env`

> `source env/bin/activate`

# Install Django and Django REST framework into the virtual environment
> `pip install -r requirements`

# Apply migrations
> `./manage.py migrate`

# Create superuser
> `./manage.py createsuperuser --email <ADMIN_EMAIL> --username <ADMIN_USERNAME>`

# Run Server
> `./manage.py runserver`
