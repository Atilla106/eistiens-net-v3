from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import (
    get_object_or_404,
    HttpResponseRedirect,
    redirect,
    render)

from common.models import SchoolYear
from .models import Account, Association, Membership
from .forms import AssociationForm


def orderKey(links):
    L = ['FB', 'TW', 'YT', 'WE', 'MA', 'OT']
    return (L.index(links.type_link))


def list(request):
    assos = {
        (asso, asso.is_member(request.user))
        for asso in Association.objects.all()
    }

    return render(
        request,
        'associations/list.html',
        {'assos': assos}
    )


def details(request, id):
    asso = get_object_or_404(Association, pk=id)
    links = sorted(asso.sociallink_set.all(), key=orderKey)
    is_member = asso.is_member(request.user)

    return render(
        request,
        'associations/details.html',
        {'asso': asso, 'links': links, 'is_member': is_member}
    )


# TODO: It will be necessary to check who the authenticated user is
@login_required
def join(request, id):
    asso = get_object_or_404(Association, pk=id)
    # No need to check if the account exists
    account = Account.objects.get(user=request.user)

    try:
        Membership.objects.create(
            account=account,
            role='OT',
            year=SchoolYear.objects.last(),
            association=asso
        )
    except IntegrityError:
        messages.error(request, "Une erreur s'est produite!")

    messages.success(request,
                     "Votre inscription est en attente de validation par le " +
                     "bureau de l'association {}".format(asso.name))
    return redirect(
            reverse('associations:details', kwargs={'id': asso.pk}))


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
