from django.contrib import admin

from . import models


class AssociationAdmin(admin.ModelAdmin):
    list_display = ['name', 'validation_state', 'subscription_cost', 'room']
    search_field = ['name', 'room']
    list_editable = ['validation_state']
    list_filter = ['validation_state']
    ordering = ['name']


admin.site.register(models.Association, AssociationAdmin)

admin.site.register(models.SocialLink)
admin.site.register(models.Refusal)
admin.site.register(models.Membership)
admin.site.register(models.Document)
