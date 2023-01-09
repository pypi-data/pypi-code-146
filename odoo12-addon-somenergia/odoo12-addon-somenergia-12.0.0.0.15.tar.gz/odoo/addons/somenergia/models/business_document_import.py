from odoo import models, api, _
import logging
logger = logging.getLogger(__name__)

class BusinessDocumentImport(models.AbstractModel):
    _inherit = 'business.document.import'

    @api.model
    def _match_product(self, product_dict, chatter_msg, seller=False):
        """ Matching product by product name customization """
        ppo = self.env['product.product']
        self._strip_cleanup_dict(product_dict)
        company_id = self._context.get('force_company') or\
            self.env.user.company_id.id
        cdomain = [('company_id', '=', company_id)]
        if product_dict.get('name'):
            product = ppo.search(cdomain + [('name', '=', product_dict['name'])], limit=1)
            if product:
                return product
        return super()._match_product(product_dict, chatter_msg, seller)

