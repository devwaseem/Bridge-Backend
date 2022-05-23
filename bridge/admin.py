from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# from bridge.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("fullname", "role")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    # "is_staff",
                    # "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("date_joined",)}),
    )
    list_display = ["email", "fullname", "role"]
    search_fields = ["fullname"]
    list_filter = ["is_active"]
    filter_horizontal = []
    ordering = ["email"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("fullname", "role", "email", "password1", "password2"),
            },
        ),
    )
