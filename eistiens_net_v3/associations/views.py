from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    HttpResponseRedirect,
    render)

from .models import Association
from .forms import AssociationForm
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


def edit(request, id):
    asso = get_object_or_404(Association, pk=id)

    if request.method == 'POST':
        form = AssociationForm(request.POST, instance=asso)
        if form.is_valid():
            form.save()
            url = reverse('associations:details', kwargs={'id': id})
            return HttpResponseRedirect(url)
        else:
            messages.error(request, 'Il y a des erreur dans le formulaire')

    form = AssociationForm(instance=asso)

    return render(
        request,
        'associations/edit.html',
        {'form': form, 'name': asso.name, 'pk': id})
