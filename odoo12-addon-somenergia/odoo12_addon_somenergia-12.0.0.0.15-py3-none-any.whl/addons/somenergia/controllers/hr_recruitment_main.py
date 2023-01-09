# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, api, models, _

class View(models.Model):
    _inherit = 'ir.ui.view'

    @api.model
    def render_template(self, template, values=None, engine='ir.qweb'):
        
        if template == 'website_hr_recruitment.apply':
            fields_data = self.env['hr.applicant'].sudo().fields_get(
                ["gender", "experience_years", "able_to_work_in_girona"])
            values["genders"] = fields_data["gender"]["selection"]
            values["experience_years_options"] = fields_data["experience_years"]["selection"]
            values["able_to_work_in_girona_options"] = fields_data["able_to_work_in_girona"]["selection"]
            values['size_contribution_text'] = self.env['hr.applicant']._TEXT_LIMIT_CONTRIBUTION_TEXT
            values['size_other_text'] = self.env['hr.applicant']._TEXT_LIMIT_OTHER_TEXT

        return super(View,self).render_template(template=template, values=values, engine=engine)
