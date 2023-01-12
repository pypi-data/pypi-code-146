from NEMO.decorators import permission_decorator

accounting_or_manager_required = permission_decorator(lambda u: u.is_active and (u.is_accounting_officer or u.is_facility_manager or u.is_superuser))