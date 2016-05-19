from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm
from .models import Profile
import pdb
# Create your views here.
def make_user(username, email, password):
    user = User.objects.create_user(username=username, email = email, password=password)
    user.save()
    p1 = Profile(user=user)
    p1.save()
    return user

def home_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    login(request, user)
                    return HttpResponseRedirect('/streamer/')
                else:
                    pass
                    # Return a 'disabled account' error message
            else:
                form = LoginForm()
                context = {'form':form}
                return render(request, 'home/home.html', context)
                # Return an 'invalid login' error message.
    else:
        #generate home page
        form = LoginForm()
        context  = {'form': form}
        return render(request, 'home/home.html', context)
def sign_up_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #pdb.set_trace()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = make_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/streamer/')
        else:
            context = {'form':form}
            return render(request, 'home/sign_up_page.html', context)
    else:
        form = RegistrationForm()
        context = {'form':form}
        return render(request, 'home/sign_up_page.html', context)
