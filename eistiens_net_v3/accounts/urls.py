from django.conf.urls import url
from django.contrib.auth.views import logout, login
from accounts import views
from accounts.forms import CustomAuthenticationForm


urlpatterns = [
#    url(r'^login$', views.login, name='login'),
    url(
        r'^login$',
        login,
        {
            'template_name': 'login.html',
            'authentication_form': CustomAuthenticationForm
        },
        name='login'
    ),
    url(r'^failed_login$', views.failed_login, name='failed_login'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]
