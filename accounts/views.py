from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import SignInForm, SignUpForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created successfully')
            return redirect('accounts:login')
        messages.error(request, "Unsuccessful registration.")
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = SignInForm()
    return render(request, 'accounts/signin.html', {'form': form})

def verify(request):
    return render(request, 'accounts/verify-email.html')