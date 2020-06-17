from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileForm

#password validation
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# for login-logout functionality
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    template_name = 'basic_app/register.html'
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user.password
            try:
                validate_password(password, user)
            except ValidationError as e:
                user_form.add_error('password',e)
                return render(request, template_name, {
                    'user_form':user_form,
                    'profile_form':profile_form
                })
            else:
                user.set_password(password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                profile.save()
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, template_name, {
                    'user_form':user_form,
                    'profile_form':profile_form
                })

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, template_name, {
            'user_form':user_form,
            'profile_form':profile_form
        })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("<h1>Your account is not active.</h1>")
        else:
            print("Username: {} and Password: {} tried to login and failed!".format(username,password))
            return HttpResponse("<h1>Invalid login details!</h1>")
    else:
        return render(request, 'basic_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("<h1>You're logged in!</h1>")

    



