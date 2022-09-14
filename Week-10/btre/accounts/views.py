from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib import auth


# Create your views here.


def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if passwords match
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect ('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )

                    user.save()
                    messages.success(request, 'Your are now registerd and can log in')
                    return redirect ('login')
        else:
            messages.error(request, 'Password  do not match') 
            return redirect('register')           

        
    else:
        return render (request, 'accounts/register.html') 


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invaled credentials, please try again')
            return redirect ('login')
    else:
        return render(request, 'accounts/login.html')   

def signout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are logged out")
    return redirect('index')        

    

