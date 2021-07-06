from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import six
import threading

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))

generate_token = TokenGenerator()
    

def send_activation_email(request, user):
    domain_name = get_current_site(request)
    email_subject = 'Verify Email Address'
    email_body = render_to_string('accounts/verification-mail.html', {
        'user': user,
        'domain': domain_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(
        subject=email_subject, 
        body=email_body,
        from_email=settings.EMAIL_FROM_USER,
        to=[user.email]
    )

    EmailThread(email).start()

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def login_forbidden(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url='app:home',
        redirect_field_name=""
    )
    if function:
        return actual_decorator(function)
    return actual_decorator