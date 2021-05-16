from django.contrib import admin

from .models import InstaToken


class InstaTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(InstaToken, InstaTokenAdmin)
