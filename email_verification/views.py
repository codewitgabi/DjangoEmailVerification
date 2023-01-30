from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Token
from django.http import HttpResponse

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
	
	token = Token.objects.create()
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
	
	user.is_active = False
	user.save()
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
		return HttpResponse("<a>Login</a> to continue")
	return HttpResponse("Token has expired")
	
	