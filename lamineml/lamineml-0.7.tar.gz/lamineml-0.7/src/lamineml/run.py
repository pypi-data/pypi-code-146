from jnius import autoclass
from plyer.platforms.android import activity
from kivy.app import App
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
intent = Intent()
intent.setAction(Intent.ACTION_VIEW)
intent.setData(Uri.parse('http://kivy.org'))
activity.startActivity(intent)


