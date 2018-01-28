from django.db import models

from accounts.models import Account
from common.models import SchoolYear


class Association(models.Model):
    VALIDATION_STATES = (
        ('MD', 'Missing documents'),
        ('SM', 'Submittable'),
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('RF', 'Refused'),
    )

    name = models.CharField(
        "Nom de l'association",
        max_length=60,
    )

    description = models.TextField(
        "Description de l'association",
        default="",
        blank=True,
    )

    validation_state = models.CharField(
        "État de la validation",
        default='MD',
        max_length=2,
        choices=VALIDATION_STATES,
    )

    logo = models.ImageField(
        "Logo de l'association",
        upload_to="associations/logo",
        default="associations/logo/default.png"
    )

    banner = models.ImageField(
        "Bannière de l'association",
        upload_to="associations/banner",
        default="associations/banner/default.png"
    )

    subscription_cost = models.IntegerField(
        "Coût de la cotisation",
        default=0,
    )

    room = models.CharField(
        "Local de l'association",
        max_length=5,
        default="",
        blank=True,
    )

    members = models.ManyToManyField(
        Account,
        through='Membership',
        through_fields=('association', 'account')
    )

    def __str__(self):
        return self.name

    def is_member(self, user):
        if user.is_authenticated():
            a = Account.objects.get(user=user)
            if (self.membership_set.filter(account=a).count() > 0):
                return True
        return False


class Membership(models.Model):
    """
    Model to represent a membership entry. It is linked to a year, meaning we
    can keep data on members from previous years.
    A member can be member of executive board, with a role, either defined
    on the DEFAULT_ROLES entry, or something else (OT), in which case the
    custom_role is filed.
    Any member cas also setup a custom role, which does not imply he's member
    of the executive board.
    By default, a member is not flagged as accepted, and it's up the the
    executive board's members to accept him.
    """
    DEFAULT_ROLES = (
        ('PR', 'Président'),
        ('VP', 'Vice-Président'),
        ('TR', 'Trésorier'),
        ('RC', 'Responsable communications'),
        ('SC', 'Secrétaire'),
        ('OT', 'Autre'),
    )

    date_subscription = models.DateField(auto_now_add=True)

    is_board = models.BooleanField(default=False)

    role = models.CharField(max_length=2, choices=DEFAULT_ROLES)

    custom_role = models.CharField(max_length=30, default="", blank=True)

    accepted = models.BooleanField(default=False)

    year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)

    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.__str__() + ' - ' + self.association.__str__()


class SocialLink(models.Model):
    PRESETS = (
        ('FB', 'Facebook'),
        ('TW', 'Twitter'),
        ('YT', 'YouTube'),
        ('WE', 'Site internet'),
        ('MA', 'Mail'),
        ('OT', 'Autre'),
    )

    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    type_link = models.CharField(max_length=2, choices=PRESETS)

    url = models.URLField()

    def __str__(self):
        return '[' + self.association.__str__() + '] ' + self.url


class Refusal(models.Model):
    """
    Object representing a comment from EISTI's administration to explain
    why an association was refused.
    """
    text = models.TextField(
        "Commentaires sur le refus",
        default="",
        blank=True,
    )

    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    comment_date = models.DateTimeField(
        "Date du commentaire",
        auto_now=True,
    )

    def __str__(self):
        return self.association.__str__()


class Document(models.Model):
    Statuses = models.FileField(
        "Status de l'association",
        upload_to='admin_doc/%Y/',
    )

    internal_regulations = models.FileField(
        "Règlement intérieur",
        upload_to='admin_doc/%Y/',
    )

    banking_account_info = models.FileField(
        "RIB",
        upload_to='admin_doc/%Y/',
    )

    insurance = models.FileField(
        "Assurances",
        upload_to='admin_doc/%Y/',
    )

    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)

    def __str__(self):
        return '[' + self.year.__str__() + '] ' + self.association.__str__()
