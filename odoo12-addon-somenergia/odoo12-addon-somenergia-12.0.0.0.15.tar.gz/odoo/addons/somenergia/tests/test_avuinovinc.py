from odoo.tests.common import TransactionCase

class TestAvuinovinc(TransactionCase):
    def test_avuinovinc(self):
        msg,leave = self.env["hr.attendance.absence"].run()
        
        # Msg check
        self.assertEqual(msg.body_html, "<p>OdooBot avui no vindrá. Ha escrit el següent missatge: </p><p>False</p>")
        self.assertEqual(msg.subject, "Avui no vinc OdooBot")
        self.assertEqual(msg.email_to, "avuinovinc@somenergia.coop")
        
        # Leave check
        self.assertEqual(leave['employee_id']['display_name'],"Mitchell Admin")
        self.assertEqual(leave['holiday_status_id']['display_name'],'Indisposició (un dia, el 2n, justificant. Inclou menors i ascendents a càrrec)')