import itchat
from itchat import Core

from itchat_desktop import components


# patch auto-inject the components into the Core class
def patch():
    Core.get_QRuuid = components.get_qr_uuid
    Core.process_login_info = components.process_login_info
    Core.check_login = components.check_login
    Core.push_login = components.push_login
    itchat.originInstance = itchat.new_instance()
