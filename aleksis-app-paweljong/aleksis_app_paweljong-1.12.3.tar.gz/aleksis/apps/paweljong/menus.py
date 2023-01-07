from django.utils.translation import gettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Register"),
            "url": "register_account_start",
            "icon": "how_to_reg",
            "validators": [
                "menu_generator.validators.is_anonymous",
            ],
        },
        {
            "name": _("Events"),
            "url": "#",
            "icon": "event_note",
            "root": True,
            "validators": [
                (
                    "aleksis.core.util.predicates.permission_validator",
                    "paweljong.view_menu",
                )
            ],
            "submenu": [
                {
                    "name": _("Vouchers"),
                    "url": "vouchers",
                    "icon": "confirmation_number",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "paweljong.view_vouchers_rule",
                        )
                    ],
                },
                {
                    "name": _("Terms"),
                    "url": "terms",
                    "icon": "gavel",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "paweljong.view_terms_rule",
                        )
                    ],
                },
                {
                    "name": _("Registration states"),
                    "url": "registration_states",
                    "icon": "list",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "paweljong.view_registration_states_rule",
                        )
                    ],
                },
                {
                    "name": _("Info mailings"),
                    "url": "info_mailings",
                    "icon": "info",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "paweljong.view_info_mailings_rule",
                        )
                    ],
                },
                {
                    "name": _("Generate participant list"),
                    "url": "generate_lists",
                    "icon": "format_list_numbered",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "paweljong.generate_lists_rule",
                        )
                    ],
                },
                {
                    "name": _("Events"),
                    "url": "manage_events",
                    "icon": "edit",
                    "validators": [
                        (
                            "aleksis.core.util.predicates.permission_validator",
                            "paweljong.change_events_rule",
                        )
                    ],
                },
            ],
        },
    ],
}
