from django.db import models

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
        null=True,
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
        null=True,
        blank=True,
    )

    banner = models.ImageField(
        "Bannière de l'association",
        upload_to="associations/banner",
        null=True,
        blank=True,
    )

    subscription_cost = models.IntegerField(
        "Coût de la cotisation",
        default=0,
    )

    room = models.CharField(
        "Local de l'association",
        max_length=5,
        null=True,
        blank=True,
    )


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


class Refusal(models.Model):
    """
    Object representing a comment from EISTI's administration to explain
    why an association was refused.
    """
    Text = models.TextField(
        "Commentaires sur le refus",
        null=True,
        blank=True,
    )

    Association = models.ForeignKey(Association, on_delete=models.CASCADE)

    Date_of_comment = models.DateTimeField(
        "Date du commentaire",
        auto_now=True,
    )


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
