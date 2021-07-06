from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return HttpResponse("Hello world! This is index page of our app.")
