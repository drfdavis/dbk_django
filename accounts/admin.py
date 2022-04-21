from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import DBKAccount
from django.utils.html import format_html

# Register your models here.
class DBKAccountAdmin(UserAdmin):
    list_display = ("username","firstname","lastname","email","phonenumber","last_login","date_joined","is_active")
    list_editable=['is_active']
    list_display_links = ("email","firstname","lastname","username")
    readonly_fields = ("last_login","date_joined")
    ordering = ('-date_joined',)
   
    filter_horizontal = ()
    list_filter=()
    fieldsets = ()



admin.site.register(DBKAccount, DBKAccountAdmin)