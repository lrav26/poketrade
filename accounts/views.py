from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from poketrade.settings import LOGIN_REDIRECT_URL
# Create your views here.
from .forms import CustomUserCreationForm, CustomErrorList

def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'

    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})

    elif request.method == 'POST':
        # Get the username or email from the POST data
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Check if the input is an email address
        if '@' in username_or_email:
            try:
                # If it's an email, get the user by email and use their username for authentication
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                user = None
        else:
            # Otherwise, it's a username
            username = username_or_email
            user = User.objects.filter(username=username).first()

        # Authenticate the user
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})

        # Authenticate with the username and password
        user = authenticate(request, username=username, password=password)

        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})

        # Log the user in
        auth_login(request, user)
        if hasattr(user, 'profile') and user.profile.is_banned:
            auth_logout(request)
            template_data['error'] = 'Your account has been banned.'
            return render(request, 'accounts/login.html', {'template_data': template_data})

        return redirect(LOGIN_REDIRECT_URL)

def signup(request):
    template_data = {'title': 'Sign Up'}

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 🚫 Banned check before logging in
            if hasattr(user, 'profile') and user.profile.is_banned:
                template_data['error'] = 'Your account has been banned.'
                template_data['form'] = form
                return render(request, 'accounts/signup.html', {'template_data': template_data})

            user.save()
            auth_login(request, user)
            return redirect(LOGIN_REDIRECT_URL)

        # If form is invalid, fall through to re-render form with errors
        template_data['form'] = form
        return render(request, 'accounts/signup.html', {'template_data': template_data})