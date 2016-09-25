from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    """
    A custom form inheriting from the Django auth form.
    User id for custom attribute (placeholder)
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': '',
            'placeholder': 'Login LDAP/Arel'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe LDAP/Arel'
        })
    )
