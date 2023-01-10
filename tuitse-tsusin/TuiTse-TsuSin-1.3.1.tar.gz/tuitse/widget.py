import json
from tuitse.html import tuitse_html


class KiamTsaNuaUi():
    def 檢查結果(self, obj):
        if not obj.檢查:
            return ''
        tinliat = json.loads(obj.檢查)
        return tuitse_html(tinliat)
