from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from .utils import email_check

@login_required(login_url='accounts:login', redirect_field_name='')
@user_passes_test(email_check, login_url='accounts:verify', redirect_field_name='')
def index(request):
    return HttpResponse("Hello world! This is index page of our app.")
