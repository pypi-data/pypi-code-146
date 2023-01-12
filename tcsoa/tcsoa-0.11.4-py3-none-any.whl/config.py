from typing import Dict


class TcSoaConfig:
    backend = None
    date_format = r'%d.%m.%Y %H:%M:%S'
    global_obj_cache_enabled = True

    __gobj_cache = dict()

    @classmethod
    def internal_handle_sd(cls, sd):
        """ Handles incoming service data, and updates the cache """
        if hasattr(sd, 'modelObjects') and sd.modelObjects:
            for uid, obj in sd.modelObjects.items():
                if uid not in cls.__gobj_cache:
                    cls.__gobj_cache[uid] = dict(uid=uid, type=obj['type'], className=obj['className'])
                for pname, pval in obj.props.items():
                    cls.__gobj_cache[uid][pname] = pval

    @classmethod
    def internal_get_prop(cls, uid: str, prop_name: str):
        props = cls.__gobj_cache.get(uid, None)
        if props:
            return props.get(prop_name, None)
        return None

    @classmethod
    def internal_get_obj(cls, uid: str) -> Dict[str, any]:
        return cls.__gobj_cache.get(uid, None)
