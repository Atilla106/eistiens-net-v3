from django.shortcuts import render, get_object_or_404

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


def details(request, id):
    asso = get_object_or_404(Association, pk=id)
    return render(request, 'associations/details.html', {'asso': asso})
