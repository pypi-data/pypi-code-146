# -*- coding: utf-8 -*-

from tabnanny import check
from odoo import models, fields, api, exceptions, _
import datetime
from pytz import timezone,utc
import pytz


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    is_present = fields.Boolean('Present Today', compute='_compute_leave_status', search='_search_present_employee')

    @api.multi
    def _search_present_employee(self, operator, value):
        holidays = self.env['hr.leave'].sudo().search([
            ('employee_id', '!=', False),
            ('state', 'not in', ['cancel', 'refuse']),
            ('date_from', '<=', datetime.datetime.utcnow()),
            ('date_to', '>=', datetime.datetime.utcnow())
        ])
        return [('id', 'not in', holidays.mapped('employee_id').ids)]

    @api.multi
    def attendance_manual(self, next_action, entered_pin=None):
        min_entrance_time = 5
        max_entrance_time = 22
        entranceTime = datetime.datetime.now(timezone('Europe/Madrid'))
        if self.attendance_state == "checked_out" and (entranceTime.hour <= min_entrance_time or entranceTime.hour >= max_entrance_time):
            return {'warning': 'No es pot fitxar abans de les 6h del mati ni més enllà de les 22h de la nit' }
        elif self.attendance_state == "checked_in":
            self.ensure_one()
            action_message = self.env.ref('hr_attendance.hr_attendance_action_greeting_message').read()[0]
            action_message['previous_attendance_change_date'] = self.last_attendance_id and (self.last_attendance_id.check_out or self.last_attendance_id.check_in) or False
            action_message['employee_name'] = self.name
            action_message['barcode'] = self.barcode
            action_message['next_action'] = next_action
            if self.user_id:
                modified_attendance = self.sudo(self.user_id.id).attendance_action_change()
            else:
                modified_attendance = self.sudo().attendance_action_change()
            action_message['attendance'] = modified_attendance.read()[0]        
            check_in_day = modified_attendance.check_in.strftime("%m/%d/%Y")
            
            if entranceTime.hour <= min_entrance_time or entranceTime.hour >= max_entrance_time:
                action_message['warning_msg'] = 'No es pot fitxar abans de les 6h del mati ni més enllà de les 22h de la nit. <br /> Aquesta sortida es fitxara a les 10'
                checkout_time = datetime.datetime.strptime(check_in_day + " 22:00:00", "%m/%d/%Y %H:%M:%S")
                localtz = timezone('Europe/Madrid')
                local_dt = localtz.localize(checkout_time,is_dst=None)
                checkout_time_utc = local_dt.astimezone(utc)
                checkout_str = checkout_time_utc.strftime("%m/%d/%Y %H:%M:%S")
                checkout_time = datetime.datetime.strptime(checkout_str, "%m/%d/%Y %H:%M:%S")
            elif  entranceTime.strftime("%m/%d/%Y") > check_in_day:
                action_message['warning_msg'] = 'El fitxatge d\'entrada va ser fa temps <br /> Aquesta sortida es marcarà el mateix dia que l\'entrada, a les 22:00'
                checkout_time = datetime.datetime.strptime(check_in_day + " 22:00:00", "%m/%d/%Y %H:%M:%S")
                localtz = timezone('Europe/Madrid')
                local_dt = localtz.localize(checkout_time,is_dst=None)
                checkout_time_utc = local_dt.astimezone(utc)
                checkout_str = checkout_time_utc.strftime("%m/%d/%Y %H:%M:%S")
                checkout_time = datetime.datetime.strptime(checkout_str, "%m/%d/%Y %H:%M:%S")
            else:
                checkout_time = datetime.datetime.now()
            modified_attendance.check_out = checkout_time
            return {'action' : action_message}
        return super().attendance_manual(next_action,entered_pin)
