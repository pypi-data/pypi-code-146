import rules
from payments import PaymentStatus

from aleksis.core.util.predicates import (
    has_any_object,
    has_global_perm,
    has_object_perm,
    has_person,
    is_site_preference_set,
)

from .models.base import Client
from .models.invoice import InvoiceGroup
from .predicates import (
    has_no_payment_variant,
    has_payment_variant,
    is_in_payment_status,
    is_own_invoice,
)

# View clients
view_clients_predicate = has_person & (
    has_global_perm("tezor.view_client") | has_any_object("tezor.view_client", Client)
)
rules.add_perm("tezor.view_clients_rule", view_clients_predicate)

# View client
view_client_predicate = has_person & (
    has_global_perm("tezor.view_client") | has_object_perm("tezor.view_client")
)
rules.add_perm("tezor.view_client_rule", view_client_predicate)

# Edit clients
edit_client_predicate = has_person & (
    has_global_perm("tezor.edit_client") | has_object_perm("tezor.edit_client")
)
rules.add_perm("tezor.edit_client_rule", edit_client_predicate)

# Create clients
create_client_predicate = has_person & (
    has_global_perm("tezor.create_client") | has_any_object("tezor.create_client", Client)
)
rules.add_perm("tezor.create_client_rule", create_client_predicate)

# Delete clients
delete_client_predicate = has_person & (
    has_global_perm("tezor.delete_client") | has_object_perm("tezor.delete_client")
)
rules.add_perm("tezor.delete_client_rule", delete_client_predicate)

# View invoice groups
view_invoice_groups_predicate = has_person & (
    has_global_perm("tezor.view_invoice_group")
    | has_any_object("tezor.view_invoice_group", InvoiceGroup)
)
rules.add_perm("tezor.view_invoice_groups_rule", view_invoice_groups_predicate)

# View invoice_group
view_invoice_group_predicate = has_person & (
    has_global_perm("tezor.view_invoice_group") | has_object_perm("tezor.view_invoice_group")
)
rules.add_perm("tezor.view_invoice_group_rule", view_invoice_group_predicate)

# Edit invoice groups
edit_invoice_group_predicate = has_person & (
    has_global_perm("tezor.edit_invoice_group") | has_object_perm("tezor.edit_invoice_group")
)
rules.add_perm("tezor.edit_invoice_group_rule", edit_invoice_group_predicate)

# Create invoice groups
create_invoice_groups_predicate = has_person & (
    has_global_perm("tezor.create_invoice_group")
    | has_any_object("tezor.create_invoice_group", InvoiceGroup)
)
rules.add_perm("tezor.create_invoice_groups_rule", create_invoice_groups_predicate)

# Delete invoice groups
delete_invoice_groups_predicate = has_person & (
    has_global_perm("tezor.delete_invoice_group")
    | has_any_object("tezor.delete_invoice_group", InvoiceGroup)
)
rules.add_perm("tezor.delete_invoice_groups_rule", delete_invoice_groups_predicate)

# Display invoice billing information
display_billing_predicate = has_person & (
    is_own_invoice
    | has_global_perm("tezor.display_billing")
    | has_object_perm("tezor.display_billing")
)
rules.add_perm("tezor.display_billing_rule", display_billing_predicate)

# Display invoice purchased items
display_purchased_items_predicate = has_person & (
    is_own_invoice
    | has_global_perm("tezor.display_purchased_items")
    | has_object_perm("tezor.display_purchased_items")
)
rules.add_perm("tezor.display_purchased_items_rule", display_purchased_items_predicate)

# Change payment variant
change_payment_variant_predicate = (
    has_person
    & is_in_payment_status(PaymentStatus.WAITING)
    & (
        (
            (is_own_invoice | is_site_preference_set("payments", "public_payments"))
            & (has_no_payment_variant | has_payment_variant("pledge"))
        )
        | has_global_perm("tezor.change_payment_variant")
        | has_object_perm("tezor.change_payment_variant")
    )
)
rules.add_perm("tezor.change_payment_variant", change_payment_variant_predicate)

# Start payment
do_payment_predicate = (
    has_person
    & (
        is_in_payment_status(PaymentStatus.WAITING)
        | is_in_payment_status(PaymentStatus.INPUT)
        | is_in_payment_status(PaymentStatus.ERROR)
        | is_in_payment_status(PaymentStatus.REJECTED)
    )
    & (
        (is_own_invoice | is_site_preference_set("payments", "public_payments"))
        | has_global_perm("tezor.do_payment")
        | has_object_perm("tezor.do_payment")
    )
)
rules.add_perm("tezor.do_payment", do_payment_predicate)

# View invoice
view_invoice_predicate = (
    has_person & is_own_invoice
    | is_site_preference_set("payments", "public_payments")
    | has_global_perm("tezor.view_invoice")
    | has_object_perm("tezor.view_invoice")
)
rules.add_perm("tezor.view_invoice_rule", view_invoice_predicate)

print_invoice_predicate = (
    view_invoice_predicate & display_billing_predicate & display_purchased_items_predicate
)
rules.add_perm("tezor.print_invoice_rule", print_invoice_predicate)

# Send invoice email
send_invoice_email_predicate = (
    has_person & is_own_invoice
    | has_global_perm("tezor.send_invoice_email")
    | has_object_perm("tezor.send_invoice_email")
)
rules.add_perm("tezor.send_invoice_email_rule", send_invoice_email_predicate)

view_own_invoices_predicate = has_person
rules.add_perm("tezor.view_own_invoices_list_rule", view_own_invoices_predicate)
