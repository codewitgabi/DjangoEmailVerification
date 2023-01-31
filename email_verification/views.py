from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Token

		
def VerifyEmail(request, form):
	subject = "Verify Your Email"
	user = form.save(commit=False)
	email = user.email
	user.is_active = False
	user.save()
	
	token = Token.objects.create(user=user)
	token.save()
	
	html_content = render_to_string("email_verification/mail.html",
		{"token": token}, request=request)

	mail = EmailMessage(
		subject,
		html_content,
		to=[email]
	)
	
	mail.content_subtype = "html"
	mail.fail_silently = False
	mail.send()

	return user


def pre_login(request, token):
	token = get_object_or_404(Token, id=token)
	if not token.has_expired:
		user = token.user
		user.is_active = True
		user.save()
		return render(
			request,
			"email_verification/pre-login-success.html",
			{"login_url": settings.LOGIN_URL}
		)
	return render(
		request, "email_verification/pre-login-failure.html")
	
	