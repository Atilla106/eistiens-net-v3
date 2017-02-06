from django.contrib import admin

from . import models


admin.site.register(models.Association)
admin.site.register(models.SocialLink)
admin.site.register(models.Refusal)
admin.site.register(models.Membership)
admin.site.register(models.Document)
