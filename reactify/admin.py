from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display


from .models import Profile, ChatRoom, Message


User = get_user_model()

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin, ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "date_joined",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    readonly_fields = (
        "last_login",
        "date_joined",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = (
        "name",
        "display_permissions",
    )
    search_fields = ("name",)

    @display(description="Permissions")
    def display_permissions(self, obj):
        return ", ".join([perm.name for perm in obj.permissions.all()])

    # Change form settings
    filter_horizontal = ("permissions",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "permissions",
                )
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(UserAdmin, ModelAdmin):

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        if obj is None:
            return False
        return request.user.id == obj.id

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        return super(ProfileAdmin, self).changeform_view(
            request, object_id, extra_context=extra_context
        )

    def response_change(self, request, obj):
        super(ProfileAdmin, self).response_change(request, obj)
        return HttpResponseRedirect(request.path + "?_continue=1")

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    ordering = ("-id",)

    search_fields = ["first_name", "last_name", "email"]
    # Display submit button in filters
    list_filter_submit = True  # Submit button at the bottom of the filter

    readonly_fields = [
        "user_permissions",
        "groups",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    ]
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "username",
                    "password",
                    ("first_name", "last_name"),
                )
            },
        ),
        (
            "Account Status",
            {
                "fields": (
                    (
                        "is_active",
                        "is_superuser",
                        "is_staff",
                        "user_permissions",
                        "groups",
                    )
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    (
                        "last_login",
                        "date_joined",
                    ),
                )
            },
        ),
    )


@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = ("name", "created_at")
    filter_horizontal = ("participants",)
    search_fields = ("name", "description")


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("user", "room", "content", "timestamp")
    list_filter = ("room",)
    search_fields = ("content", "user__username", "room__name")
