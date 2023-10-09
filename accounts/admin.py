from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Account


class Accountadmin(UserAdmin):
    list_display = (
        "is_staff",
        "is_bdo",
        "is_admin",
        "date_joined",
        "first_name",
        "username",
        "last_login",
    )
    search_fields = ("username", "first_name")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, Accountadmin)
