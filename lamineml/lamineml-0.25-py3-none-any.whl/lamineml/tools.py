from kivy.app import App
from jnius import autoclass
from plyer.platforms.android import activity
class main:
 def open_browser(self,url):
    self.url =url
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    intent = Intent()
    intent.setAction(Intent.ACTION_VIEW)
    intent.setData(Uri.parse(self.url))
    activity.startActivity(intent)
 def open_app(self,p):
    self.p =p
 


    s=activity.getPackageManager().getLaunchIntentForPackage(p)
    activity.startActivity(s)
 def open_setting(self):
     intent=autoclass("android.content.Intent")
     settings = autoclass("android.provider.Settings")
     activity.startActivity(intent(settings.ACTION_LOCATION_SOURCE_SETTINGS))
main=main()




