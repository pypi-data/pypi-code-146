from jnius import autoclass
from plyer.platforms.android import activity
class share():
    def run(self,s):      
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(s))
        activity.startActivity(intent)


