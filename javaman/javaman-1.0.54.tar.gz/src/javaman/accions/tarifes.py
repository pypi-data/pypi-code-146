from javaman.connexio import JManCon


class Tarifes:
    __slots__ = '_con'

    _url_get_tip_tarifes = '/tip_tarifes'
    _url_get_tarifes = '/tip_tarifes/{tip_tarifa_id}/ex'

    def __init__(self, con: JManCon):
        self._con = con

    def get_tip_tarifes(self):
        req = self._con.get(url=self._url_get_tip_tarifes)
        return req.json()

    def get_tarifes(self, p_tip_tarifa_id: int):
        req = self._con.get(url=self._url_get_tarifes.format(tip_tarifa_id=p_tip_tarifa_id))
        return req.json()
