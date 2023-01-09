
from odoo import models, fields, _
import logging
import datetime

_logger = logging.getLogger(__name__)


class HrAttendanceAbsence(models.TransientModel):
    _name = 'hr.attendance.absence'

    absence_message = fields.Text("Missatge", help="Missatge que s'enviara al grup de laboral",
                                  default="Avui no em trobo amb forces per assistir a la feina.")

    def run(self):
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)])

        # Create Leave
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        lt_avuinovinc = self.env['ir.model.data'].get_object_reference('somenergia','leave_avui_no_vinc')[1]

        leave_values = {
            'holiday_type': 'employee',
            'holiday_status_id': lt_avuinovinc,
            'request_date_from': today,
            'request_date_to': today,
            'request_date_from_period': 'am',
            'name': self.absence_message,
            'employee_id': employee_id.id,
            'number_of_days': 1,
            'message_attachment_count': 0
        }

        self.env['hr.leave'].create(leave_values)

        # Send Email
        mail_html = "<p>{} avui no vindrá. Ha escrit el següent missatge: </p><p>{}</p>".format(
            user.display_name,
            self.absence_message)

        mail_values = {
            'body_html': mail_html,
            'subject':  'Avui no vinc {}'.format(user.display_name),
            'email_from': user.partner_id.email or user.company_id.catchall or user.company_id.email,
            'email_to': 'avuinovinc@somenergia.coop',
        }
        try:
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()
        except Exception:
            _logger.exception("Unable to send email when report a 'Avui No vinc' leave")

        return True
