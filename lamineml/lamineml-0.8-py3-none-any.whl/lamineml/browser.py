from jnius import autoclass
from plyer.platforms.android import activity
from kivy.app import App
class main():
 def open(self,url)
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    intent = Intent()
    intent.setAction(Intent.ACTION_VIEW)
    intent.setData(Uri.parse(url))
    activity.startActivity(intent)


