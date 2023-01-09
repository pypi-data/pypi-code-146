# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class HrAttendanceInherit(models.Model):
    _inherit = "hr.attendance"
    comments = fields.Char(string="Comments", size=100)