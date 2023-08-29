from django.shortcuts import render, redirect
from .forms import RegisterForm, UserBioForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from .models import UserBio

def signup(request):
    form = RegisterForm
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form':form
    }
    return render(request, 'authentication/signup.html', context)

def signin(request):
    if request.method == "POST":
        reg_no = request.POST.get('reg_num')
        password = request.POST.get('password')
        user = authenticate(request, reg_no=reg_no, password=password)

        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                if user.id:
                    try:
                        UserBio.objects.get(user_id=user.id)
                        return redirect('/')
                    except UserBio.DoesNotExist:
                        return redirect('createbio')
        else:
            return HttpResponse('An error occurred :(\nTry signing in again <a href="/auths/login/">here</a>')
    context = {}
    return render(request, 'authentication/signin.html', context)

def signout(request):
    logout(request)
    return redirect('login')


def createbio(request):
    form = UserBioForm
    if request.method == "POST":
        form = UserBioForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('/')
    else:
        form = UserBioForm()
    context = {
        'form':form
    }
    return render(request, 'authentication/createbio.html', context)