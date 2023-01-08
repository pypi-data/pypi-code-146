from jnius import autoclass
from plyer.platforms.android import activity
from kivy.app import App
class main:
 def open_browser(self,*args):
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    intent = Intent()
    intent.setAction(Intent.ACTION_VIEW)
    intent.setData(Uri.parse(args))
    activity.startActivity(intent)
 def open_app(self,*args):

    s=activity.getPackageManager().getLaunchIntentForPackage(args)
    activity.startActivity(s)
 def open_setting(self,*args):
     settings = autoclass("android.provider.Settings")
     activity.startActivity(intent(settings.ACTION_LOCATION_SOURCE_SETTINGS))




