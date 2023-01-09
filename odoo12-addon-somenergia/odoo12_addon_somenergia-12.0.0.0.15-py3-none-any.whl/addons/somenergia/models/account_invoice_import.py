from odoo import models, api
from datetime import datetime


class AccountInvoiceImport(models.TransientModel):
    _inherit = 'account.invoice.import'

    @api.model
    def _prepare_create_invoice_vals(self, parsed_inv, import_config=False):
        (vals, import_config) = (
            super()._prepare_create_invoice_vals(parsed_inv, import_config)
        )
        vals['name'] = parsed_inv.get('name')
        import_config = self.import_config_id.convert_to_import_config()
        if import_config['invoice_line_method'] == '1line_static_product':
            date_string = parsed_inv['lines'][0]['date']
            date_parsed = datetime.strptime(date_string,'%Y-%m-%d').strftime('%m/%Y')
            vals['invoice_line_ids'][0][2]['name'] += ' ' + date_parsed

        return vals, import_config

    @api.model
    def parse_facturae_invoice(self, xml_root, xsd_file):
        parsed_inv = super().parse_facturae_invoice(xml_root, xsd_file)
        invoice = xml_root.find('Invoices/Invoice')
        inv_series_code = invoice.find('InvoiceHeader/InvoiceSeriesCode').text
        parsed_inv['name'] = inv_series_code
        parsed_inv['ref'] = inv_series_code
        return parsed_inv


    def facturae_parse_line(self, xml_root, invoice, line):
        ret_vals = super().facturae_parse_line(xml_root, invoice, line)
        product_name = False
        if line.find('ItemDescription') is not None:
            product_name = line.find('ItemDescription').text

        line_info = False
        date_orig = False
        try:
            date_orig = invoice.find('InvoiceIssueData/InvoicingPeriod/StartDate').text
            date_parsed = datetime.strptime(date_orig,'%Y-%m-%d').strftime('%m/%Y')
            line_info = '{} {}'.format(product_name, date_parsed)
        except Exception as e:
            raise e

        ret_vals.update({'name': line_info, 'date': date_orig,
                         'product': {'code': ret_vals['product']['code'], 'name': product_name}
                        })

        return ret_vals
