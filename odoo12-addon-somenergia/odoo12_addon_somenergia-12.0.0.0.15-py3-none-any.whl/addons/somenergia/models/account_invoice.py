# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _check_duplicate_customer_reference(self):
        for invoice in self:
            # refuse to validate a customer bill/credit note if there already exists one with the same reference for the same partner,
            # because it's probably a double encoding of the same bill/credit note
            if invoice.type in ('out_invoice', 'out_refund') and invoice.reference:
                if self.search([('type', '=', invoice.type), ('reference', '=', invoice.reference), ('company_id', '=', invoice.company_id.id), ('commercial_partner_id', '=', invoice.commercial_partner_id.id), ('id', '!=', invoice.id)]):
                    raise UserError(_("Duplicated customer reference detected. You probably encoded twice the same customer bill/credit note."))

    @api.multi
    def invoice_validate(self):
        self._check_duplicate_customer_reference()
        return super().invoice_validate()

