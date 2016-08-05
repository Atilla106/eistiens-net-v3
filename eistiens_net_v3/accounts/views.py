from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib import messages

from .forms import CustomAuthenticationForm

User = get_user_model()


def login(request):
    """
    Custom login view, so we can have message sending on a
    successful login.
    """
    redirect_to = request.POST.get(
        'next',
        default=request.GET.get('next', default=settings.LOGIN_REDIRECT_URL)
    )

    if request.user.is_authenticated:
        return redirect(redirect_to)
    elif request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.add_message(
                request,
                messages.SUCCESS,
                'Bienvenue, ' + form.get_user().username + " !"
            )
            return redirect(redirect_to)
    else:
        form = CustomAuthenticationForm(request)

    context = {
        'form': form,
        'next': redirect_to
    }

    return render(request, 'login.html', context=context)
