# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class AccountJournal(models.Model): 
    _inherit = "account.journal"
 
    code = fields.Char(string='Short Code', size=32, required=True, help="The journal entries of this journal will be named using this prefix.")
