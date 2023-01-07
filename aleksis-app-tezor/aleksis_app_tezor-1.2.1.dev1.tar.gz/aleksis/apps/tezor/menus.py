from django.utils.translation import gettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Payments and Money"),
            "url": "#",
            "root": True,
            "svg_icon": "mdi:piggy-bank",
            "validators": [
                "menu_generator.validators.is_authenticated",
                "aleksis.core.util.core_helpers.has_person",
            ],
            "submenu": [
                {
                    "name": _("Manage clients"),
                    "url": "clients",
                    "svg_icon": "mdi:domain",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "tezor.can_view_clients",
                        )
                    ],
                },
                {
                    "name": _("My invoices"),
                    "url": "personal_invoices",
                    "svg_icon": "fa6-solid:file-invoice-dollar",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
            ],
        }
    ]
}
