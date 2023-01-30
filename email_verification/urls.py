from django.urls import path
from . import views


app_name = "verify_email"
urlpatterns = [
	path("", views.register, name="register"),
	path("<str:token>/", views.pre_login, name="pre-login"),
]