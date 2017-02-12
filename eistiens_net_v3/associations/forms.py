from django import forms

from .models import Association


class AssociationForm(forms.ModelForm):
    class Meta:
        model = Association
        fields = ['description', 'subscription_cost', 'logo', 'banner', 'room']
