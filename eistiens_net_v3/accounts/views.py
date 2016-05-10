from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
# Create your views here.


def login(request):
    user = auth.authenticate(
        username=request.POST['login'],
        password=request.POST['password']
    )
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        return HttpResponseRedirect('/accounts/failed_login')


def login_page(request):
    return render(request, 'login.html')


def failed_login(request):
    return render(
        request,
        'login.html',
        {
                'request': request,
                'login_failed': True,
        })
