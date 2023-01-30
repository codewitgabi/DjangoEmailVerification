from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Token

User = get_user_model()

class SignupForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["username"].help_text = None
		self.fields["password1"].help_text = None
		
		
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]
		
		
def sendMail(form):
	subject = "Verify Your Email"
	user = form.save(commit=False)
	email = user.email
	user.is_active = False
	user.save()
	
	token = Token.objects.create(user=user)
	token.save()
	
	html_content = render_to_string("mail.html", {"token": token})

	mail = EmailMessage(
		subject,
		html_content,
		to=[email]
	)
	
	mail.content_subtype = "html"
	mail.fail_silently = False
	mail.send()

	return user


def register(request):
	t = Token.objects.all().last()
	form = SignupForm()
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			sendMail(form)
			return redirect("verify_email:register")
	return render(request, "signup.html", {"form": form, "token": t})
	

def pre_login(request, token):
	t = Token.objects.get(id=token)
	if not t.has_expired:
		user = t.user
		user.is_active = True
		user.save()
		return render(request, "pre-login-success.html")
	return render(request, "pre-login-failure.html")
	
	