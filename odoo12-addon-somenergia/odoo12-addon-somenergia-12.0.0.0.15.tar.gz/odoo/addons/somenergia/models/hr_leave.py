# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.addons.hr_holidays.models.hr_leave import DummyAttendance
from datetime import datetime
from pytz import timezone, UTC

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    @api.multi
    def unlink(self):
        ''' Employees can delete their owns leaves even when they are validated
        '''
        for holiday in self:
            if holiday.date_to < datetime.today():
                continue
            if holiday.state not in ['draft', 'cancel', 'confirm', 'refuse']:
                holiday.sudo().action_refuse()
            if holiday.state not in ['draft', 'cancel', 'confirm']:
                holiday.sudo().action_draft()

        res = super(HolidaysRequest, self).unlink()
        if res:
            return {
		'name': _('New Request'),
		'view_type': 'calendar',
		'view_mode': 'calendar',
		'res_model': 'hr.leave',
		'view_id': 'hr_holidays.hr_leave_view_calendar',
		'type': 'ir.actions.act_window',
		'target': 'current',
		'nodestroy': True
	    }

    @api.model
    def get_leaves(self, start_date, end_date):
        """
        This function returns leaves from start_date to end_date in the following
        format: {'worker': email, 'start_time': '2021-12-30','end_time': '2021-12-31'}
        """
        res = []
        resources_calendar_leaves_model = self.env["resource.calendar.leaves"]
        resource_resource_model = self.env["resource.resource"]
        search_params = [
            ('date_to','>=', start_date),
            ('date_from', '<=', end_date),
            ('holiday_id','!=', False)
        ]
        leaves = resources_calendar_leaves_model.search(search_params)

        for leave_id in leaves.ids:
            leave_data = resources_calendar_leaves_model.browse(leave_id)
            worker = leave_data.resource_id.user_id.email
            res.append({
                'worker': worker,
                'start_time': leave_data.date_from,
                'end_time': leave_data.date_to
            })

        return res

    @api.onchange('request_date_from_period', 'request_hour_from', 'request_hour_to',
                  'request_date_from', 'request_date_to',
                  'employee_id')
    def _onchange_request_parameters(self):
        if not self.request_date_from:
            self.date_from = False
            return

        if self.request_unit_half or self.request_unit_hours:
            self.request_date_to = self.request_date_from

        if not self.request_date_to:
            self.date_to = False
            return

        domain = [
            ('calendar_id', '=', self.employee_id.resource_calendar_id.id or self.env.user.company_id.resource_calendar_id.id),
        ]
        if self.request_unit_half:
            domain += [
                ('date_from', '<=', self.date_from),
                '|', ('date_to', '>=', self.date_to), ('date_to', '=', False)
            ]
        attendances = self.env['resource.calendar.attendance'].read_group(domain, ['ids:array_agg(id)', 'hour_from:min(hour_from)', 'hour_to:max(hour_to)', 'dayofweek', 'day_period'], ['dayofweek', 'day_period'], lazy=False)

        # Must be sorted by dayofweek ASC and day_period DESC
        attendances = sorted([DummyAttendance(group['hour_from'], group['hour_to'], group['dayofweek'], group['day_period']) for group in attendances], key=lambda att: (att.dayofweek, att.day_period != 'morning'))

        default_value = DummyAttendance(0, 0, 0, 'morning')

        # find first attendance coming after first_day
        attendance_from = next((att for att in attendances if int(att.dayofweek) >= self.request_date_from.weekday()), attendances[0] if attendances else default_value)
        # find last attendance coming before last_day
        attendance_to = next((att for att in reversed(attendances) if int(att.dayofweek) <= self.request_date_to.weekday()), attendances[-1] if attendances else default_value)

        if self.request_unit_half:
            if self.request_date_from_period == 'am':
                hour_from = float_to_time(attendance_from.hour_from)
                hour_to = float_to_time(attendance_from.hour_to)
            else:
                hour_from = float_to_time(attendance_to.hour_from)
                hour_to = float_to_time(attendance_to.hour_to)
        elif self.request_unit_hours:
            # This hack is related to the definition of the field, basically we convert
            # the negative integer into .5 floats
            hour_from = float_to_time(abs(self.request_hour_from) - 0.5 if self.request_hour_from < 0 else self.request_hour_from)
            hour_to = float_to_time(abs(self.request_hour_to) - 0.5 if self.request_hour_to < 0 else self.request_hour_to)
        elif self.request_unit_custom:
            hour_from = self.date_from.time()
            hour_to = self.date_to.time()
        else:
            hour_from = float_to_time(attendance_from.hour_from)
            hour_to = float_to_time(attendance_to.hour_to)
        self.date_from = timezone(self.tz).localize(datetime.combine(self.request_date_from, hour_from)).astimezone(UTC).replace(tzinfo=None)
        self.date_to = timezone(self.tz).localize(datetime.combine(self.request_date_to, hour_to)).astimezone(UTC).replace(tzinfo=None)
        self._onchange_leave_dates()

    @api.multi
    @api.depends('number_of_days')
    def _compute_number_of_hours_display(self):
        for holiday in self:
            calendar = holiday.employee_id.resource_calendar_id or self.env.user.company_id.resource_calendar_id
            if holiday.date_from and holiday.date_to:
                number_of_hours = calendar.get_work_hours_count(holiday.date_from, holiday.date_to)
                holiday.number_of_hours_display = number_of_hours or (holiday.number_of_days * HOURS_PER_DAY)
            else:
                holiday.number_of_hours_display = 0

