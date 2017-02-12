from django.shortcuts import render

from .models import Association
from accounts.models import Account


def list(request):
    assos = Association.objects.all()
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
    else:
        account = None

    return render(
        request,
        'associations/list.html',
        {'assos': assos, 'account': account}
    )
