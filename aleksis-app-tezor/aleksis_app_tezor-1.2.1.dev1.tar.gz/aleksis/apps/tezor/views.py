from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.views.generic.detail import DetailView

from django_tables2.views import RequestConfig, SingleTableView
from djp_sepa.models import SEPAMandate
from payments import PaymentStatus, RedirectNeeded
from rules.contrib.views import PermissionRequiredMixin

from aleksis.core.mixins import AdvancedCreateView, AdvancedDeleteView, AdvancedEditView
from aleksis.core.views import RenderPDFView

from .filters import InvoicesFilter
from .forms import EditClientForm, EditInvoiceGroupForm, InvoicesActionForm
from .models.base import Client
from .models.invoice import Invoice, InvoiceGroup
from .tables import ClientsTable, InvoiceGroupsTable, InvoicesTable
from .tasks import email_invoice


class GetInvoicePDF(PermissionRequiredMixin, RenderPDFView):

    permission_required = "tezor.print_invoice_rule"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        invoice = Invoice.objects.get(token=self.kwargs["token"])
        self.template_name = invoice.group.template_name
        context["invoice"] = invoice

        return context

    def has_permission(self):

        invoice = Invoice.objects.get(token=self.kwargs["token"])

        perms = self.get_permission_required()
        return self.request.user.has_perms(perms, invoice)


class DoPaymentView(PermissionRequiredMixin, View):

    model = Invoice
    permission_required = "tezor.do_payment_rule"
    template_name = "tezor/invoice/payment.html"

    def dispatch(self, request, token):
        self.object = get_object_or_404(self.model, token=token)

        new_variant = request.GET.get("variant", None)
        if new_variant:
            if request.user.has_perm("tezor.change_payment_variant", self.object):
                if new_variant in dict(self.object.get_variant_choices()).keys():
                    self.object.variant = new_variant
                    self.object.save()
                else:
                    raise SuspiciousOperation()
            else:
                raise PermissionDenied()

        if self.object.status not in [
            PaymentStatus.WAITING,
            PaymentStatus.INPUT,
            PaymentStatus.REJECTED,
        ]:
            return redirect(self.object.get_success_url())

        try:
            form = self.object.get_form(data=request.POST or None)
        except RedirectNeeded as redirect_to:
            return redirect(str(redirect_to))

        context = {
            "form": form,
            "payment": self.object,
        }

        return render(request, self.template_name, context)


class ClientListView(PermissionRequiredMixin, SingleTableView):
    """Table of all clients."""

    model = Client
    table_class = ClientsTable
    permission_required = "tezor.view_clients_rule"
    template_name = "tezor/client/list.html"


@method_decorator(never_cache, name="dispatch")
class ClientCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for clients."""

    model = Client
    form_class = EditClientForm
    permission_required = "tezor.create_client_rule"
    template_name = "tezor/client/create.html"
    success_url = reverse_lazy("clients")
    success_message = _("The client has been created.")


@method_decorator(never_cache, name="dispatch")
class ClientEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for clients."""

    model = Client
    form_class = EditClientForm
    permission_required = "tezor.edit_client_rule"
    template_name = "tezor/client/edit.html"
    success_url = reverse_lazy("clients")
    success_message = _("The client has been saved.")


class ClientDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete view for client."""

    model = Client
    permission_required = "tezor.delete_client_rule"
    template_name = "core/pages/delete.html"
    success_url = reverse_lazy("clients")
    success_message = _("The client has been deleted.")


class ClientDetailView(PermissionRequiredMixin, DetailView):

    model = Client
    permission_required = "tezor.view_client_rule"
    template_name = "tezor/client/full.html"

    def get_context_data(self, object):
        context = super().get_context_data()

        invoice_groups = object.invoice_groups.all()
        invoice_groups_table = InvoiceGroupsTable(invoice_groups)
        RequestConfig(self.request).configure(invoice_groups_table)
        context["invoice_groups_table"] = invoice_groups_table

        return context


class InvoiceGroupDetailView(PermissionRequiredMixin, DetailView):

    model = InvoiceGroup
    permission_required = "tezor.view_invoice_group_rule"
    template_name = "tezor/invoice_group/full.html"

    def post(self, request, *args, **kwargs):
        r = super().get(request, *args, **kwargs)
        if self.invoices_action_form.is_valid():
            action = self.invoices_action_form.cleaned_data["action"]
            if request.user.has_perm(action.permission):
                r = self.invoices_action_form.execute() or r

        return r

    def get_context_data(self, object):
        context = super().get_context_data()

        qs = object.invoices.all()
        invoices_filter = InvoicesFilter(self.request.GET, qs)
        context["filter"] = invoices_filter

        invoices = invoices_filter.qs
        invoices_table = InvoicesTable(invoices)
        RequestConfig(self.request).configure(invoices_table)
        context["invoices_table"] = invoices_table

        self.invoices_action_form = InvoicesActionForm(
            self.request, self.request.POST or None, queryset=invoices
        )
        context["action_form"] = self.invoices_action_form

        return context


@method_decorator(never_cache, name="dispatch")
class InvoiceGroupCreateView(PermissionRequiredMixin, AdvancedCreateView):
    """Create view for invoice_groups."""

    model = InvoiceGroup
    form_class = EditInvoiceGroupForm
    permission_required = "tezor.create_invoice_groups_rule"
    template_name = "tezor/invoice_group/create.html"
    success_message = _("The invoice group has been created.")

    def form_valid(self, form):
        client = Client.objects.get(id=self.kwargs["pk"])
        InvoiceGroup.objects.create(
            client=client,
            name=form.cleaned_data["name"],
            template_name=form.cleaned_data["template_name"],
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("client_by_pk", args=[self.object.client.pk])


@method_decorator(never_cache, name="dispatch")
class InvoiceGroupEditView(PermissionRequiredMixin, AdvancedEditView):
    """Edit view for invoice_groups."""

    model = InvoiceGroup
    form_class = EditInvoiceGroupForm
    permission_required = "tezor.edit_invoice_group_rule"
    template_name = "tezor/invoice_group/edit.html"
    success_url = reverse_lazy("invoice_groups")
    success_message = _("The invoice group has been saved.")


class InvoiceGroupDeleteView(PermissionRequiredMixin, AdvancedDeleteView):
    """Delete view for invoice_group."""

    model = InvoiceGroup
    permission_required = "tezor.delete_invoice_group_rule"
    template_name = "core/pages/delete.html"
    success_url = reverse_lazy("invoice_groups")
    success_message = _("The invoice group has been deleted.")


class InvoiceDetailView(PermissionRequiredMixin, DetailView):

    model = Invoice
    slug_field = "token"
    permission_required = "tezor.view_invoice_rule"
    template_name = "tezor/invoice/full.html"


class SendInvoiceEmail(PermissionRequiredMixin, View):

    permission_required = "tezor.send_invoice_email_rule"

    def get(self, request, token):
        email_invoice.delay(token)

        url = request.META.get("HTTP_REFERRER")
        if not url:
            url = Invoice.objects.get(token=token).get_absolute_url()

        return redirect(url)


class InvoiceGroupSEPAXML(PermissionRequiredMixin, View):

    model = Invoice
    permission_required = "tezor.get_sepa_xml_rule"

    def get(self, request, pk):
        qs = SEPAMandate.objects.filter(payment__group__pk=pk)

        sepa = SEPAMandate.as_sepadd(qs=qs)
        xml = sepa.export(pretty_print=true).decode()

        return HttpResponse(
            xml,
            headers={
                "Content-Type": "text/xml",
                "Content-Disposition": 'attachment; filename="sepa.xml"',
            },
        )


class MyInvoicesListView(PermissionRequiredMixin, SingleTableView):
    """Table of all invoices belonging to a user."""

    model = Invoice
    table_class = InvoicesTable
    permission_required = "tezor.view_own_invoices_list_rule"
    template_name = "tezor/invoice/list.html"

    def get_queryset(self, *args, **kwargs):
        invoices = self.model.objects.filter(person=self.request.user.person)

        return invoices
