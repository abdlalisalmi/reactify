from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def has_permission(request, app_label, model_name):
    return request.user.has_perm(f"{app_label}.view_{model_name}")


UNFOLD = {
    "SITE_TITLE": "Reactify",
    "SITE_HEADER": "Reactify",
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: "https://res.cloudinary.com/djr3obtg6/image/upload/v1710331091/logo_avd7to.png",
    "SITE_SYMBOL": "favorite",  # symbol from icon set
    # "LOGIN": {
    #     "image": lambda r: "https://i.imgur.com/aIkz2KI.png",
    # },
    # "DASHBOARD_CALLBACK": "cantina.views.dashboard_callback",
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("My Profile"),
                        "icon": "person",
                        "link": lambda request: reverse_lazy(
                            "admin:reactify_profile_change",
                            args=[request.user.id],
                        ),
                        "permission": lambda request: request.user.is_staff,
                    },
                ],
            },
            {
                "title": _("Access Management"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: has_permission(
                            request, "authentication", "user"
                        ),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: has_permission(
                            request, "auth", "group"
                        ),
                    },
                ],
            },
            {
                "title": _("Content Management"),
                "separator": True,  # Top border
                "items": [
                    {
                        "title": _("Chat Rooms"),
                        "icon": "chat",
                        "link": reverse_lazy("admin:reactify_chatroom_changelist"),
                        "permission": lambda request: has_permission(
                            request, "reactify", "chatroom"
                        ),
                    },
                    {
                        "title": _("Messages"),
                        "icon": "forum",
                        "link": reverse_lazy("admin:reactify_message_changelist"),
                        "permission": lambda request: has_permission(
                            request, "reactify", "message"
                        ),
                    },
                ],
            },
        ],
    },
}
