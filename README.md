# Installation
This project is a simple one to use for your django project to implement User email verification. Follow each step below to install it.

`pip install -r requirements.txt`

This will install everything in the `requirements.txt` file.

Go to your command prompt or terminal and run the following commands

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

# settings.py Configuration
When using the email verification, you need to specify `LOGIN_URL` for your project. This will be used to redirect users after their email has been verified.

`LOGIN_URL = "path-to-login"`
