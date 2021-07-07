from accounts.utils import send_activation_email
from allauth.socialaccount.models import SocialAccount
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required

@login_required(login_url='accounts:login', redirect_field_name='')
def index(request):
    if SocialAccount.objects.filter(user=request.user).exists():
        if not request.user.is_email_verified:
            send_activation_email(request, request.user)
    if not request.user.is_email_verified:
        return redirect('accounts:verify')
    return HttpResponse("Hello world! This is index page of our app.")
