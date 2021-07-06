from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('register/', views.signup, name='register'),
    path('verify/', views.verify, name='verify'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('logout/', views.signout, name='logout')
]
