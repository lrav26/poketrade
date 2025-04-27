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
        username_or_email = request.POST['username']
        password = request.POST['password']

        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                user = None
        else:
            username = username_or_email
            user = User.objects.filter(username=username).first()

        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})

        user = authenticate(request, username=username, password=password)

        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})

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

            if hasattr(user, 'profile') and user.profile.is_banned:
                template_data['error'] = 'Your account has been banned.'
                template_data['form'] = form
                return render(request, 'accounts/signup.html', {'template_data': template_data})

            user.save()
            auth_login(request, user)
            return redirect(LOGIN_REDIRECT_URL)

        template_data['form'] = form
        return render(request, 'accounts/signup.html', {'template_data': template_data})