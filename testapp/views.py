from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from email_verification.views import verify_email

User = get_user_model()

class SignupForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].help_text = None
		self.fields["password1"].help_text = None
		
		
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]
		

def register(request):
	form = SignupForm()
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			verify_email(request, form)
	return render(request, "testapp/signup.html", {"form": form})
	
	