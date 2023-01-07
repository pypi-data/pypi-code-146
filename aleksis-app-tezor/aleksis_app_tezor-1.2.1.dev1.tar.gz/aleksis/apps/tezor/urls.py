from django.urls import include, path

from . import views

urlpatterns = [
    path("payments/", include("payments.urls")),
    path("payments/sepa/", include("djp_sepa.urls")),
    path("invoice/<str:token>/print/", views.GetInvoicePDF.as_view(), name="print_invoice"),
    path("invoice/<str:token>/pay", views.DoPaymentView.as_view(), name="do_payment"),
    path(
        "clients/",
        views.ClientListView.as_view(),
        name="clients",
    ),
    path(
        "client/create/",
        views.ClientCreateView.as_view(),
        name="create_client",
    ),
    path(
        "client/<int:pk>/edit/",
        views.ClientEditView.as_view(),
        name="edit_client_by_pk",
    ),
    path(
        "client/<int:pk>/delete/",
        views.ClientDeleteView.as_view(),
        name="delete_client_by_pk",
    ),
    path(
        "client/<int:pk>/",
        views.ClientDetailView.as_view(),
        name="client_by_pk",
    ),
    path(
        "client/<int:pk>/invoice_groups/create/",
        views.InvoiceGroupCreateView.as_view(),
        name="create_invoice_group",
    ),
    path(
        "invoice_group/<int:pk>/edit/",
        views.InvoiceGroupEditView.as_view(),
        name="edit_invoice_group_by_pk",
    ),
    path(
        "invoice_group/<int:pk>/",
        views.InvoiceGroupDetailView.as_view(),
        name="invoice_group_by_pk",
    ),
    path(
        "invoice_group/<int:pk>/delete/",
        views.InvoiceGroupDeleteView.as_view(),
        name="delete_invoice_group_by_pk",
    ),
    path("invoices/my/", views.MyInvoicesListView.as_view(), name="personal_invoices"),
    path(
        "invoice/<str:slug>/",
        views.InvoiceDetailView.as_view(),
        name="invoice_by_token",
    ),
    path(
        "invoice/<str:token>/send/",
        views.SendInvoiceEmail.as_view(),
        name="send_invoice_by_token",
    ),
]
