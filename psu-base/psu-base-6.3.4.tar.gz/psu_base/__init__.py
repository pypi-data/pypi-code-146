from django.conf import settings

__version__ = "6.3.4"
name = "psu_base"

default_app_config = "psu_base.apps.PsuTemplateConfig"

# Default settings
_DEFAULTS = {
    "PSU_BASE_VERSION": __version__,
    "FINTI_URL": "https://sf-stage.oit.pdx.edu",
    "FINTI_SIMULATE_CALLS": False,  # Simulate Finti calls (i.e. when not on VPN)
    "FINTI_SAVE_RESPONSES": False,  # Save/record actual Finti responses for offline use?
    "AUTHORIZE_GLOBAL": False,  # Allow authorizing for other apps?
    # Admin Menu Items
    "PSU_BASE_ADMIN_LINKS": [
        {
            "url": "psu:emails",
            "label": "Email Log",
            "icon": "fa-envelope-o",
            "authorities": "~PowerUser",
        },
        {
            "url": "psu:features",
            "label": "Feature Toggles",
            "icon": "fa-plug",
            "authorities": "~SuperUser+features",
        },
        {
            "url": "psu:audit",
            "label": "Audit Events",
            "icon": "fa-id-card-o",
            "authorities": "~SecurityOfficer+auditor",
        },
        {
            "url": "psu:audit_xss",
            "label": "XSS Attempts",
            "icon": "fa-user-secret",
            "authorities": "~SecurityOfficer+auditor",
        },

        {
            "label": "Developer Resources",
            "icon": "fa-wrench",
            "authorities": "developer",
            "menu": [
                {"url": "psu:test", "label": "Status Page", "icon": "fa-medkit"},
                {
                    "url": "psu:errors",
                    "label": "Error Log",
                    "icon": "fa-exclamation-triangle",
                    "authorities": "developer",
                },
                {
                    "url": "psu:finti",
                    "label": "Finti Interface",
                    "icon": "fa-laptop",
                    "authorities": "developer",
                    "feature": "finti_console",
                    "nonprod_only": True,
                },
                {
                    "url": "psu:session",
                    "label": "Session Contents",
                    "icon": "fa-microchip",
                    "authorities": "developer",
                },
                {
                    "url": "psu:email",
                    "label": "Send Test Email",
                    "icon": "fa-paper-plane-o",
                    "authorities": "developer",
                },
                {
                    "url": "psu:scripts",
                    "label": "Admin Script",
                    "icon": "fa-terminal",
                    "authorities": "developer",
                    "feature": "admin_script",
                },
                {
                    "url": "psu:export",
                    "label": "Database Export",
                    "icon": "fa-database",
                    "authorities": "developer",
                    "feature": "database_export",
                },
                {
                    "url": "psu:downtimes",
                    "label": "Downtimes",
                    "icon": "fa-bed",
                    "authorities": "developer",
                },
                {
                    "url": "psu:variables",
                    "label": "Variables",
                    "icon": "fa-code",
                    "authorities": "developer",
                },
            ],
        },
    ],
}

# Assign default setting values
for key, value in _DEFAULTS.items():
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except:
        pass
