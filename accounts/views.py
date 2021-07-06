from django.shortcuts import render
from django.http.response import HttpResponse

def signin(request):
    return HttpResponse("This is log in page!")

def signup(request):
    return HttpResponse("This is register page!")

def verify(request):
    return HttpResponse("This is verify-email page!")
