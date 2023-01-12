from javaman.connexio import JManCon


class Recepcions:
    __slots__ = '_con'

    _url_proveidors = '/recepcions/proveidors'
    _url_proveidor = '/recepcions/proveidors/{proveidor_id}'
    _url_proveidor_articles = '/recepcions/proveidors/{proveidor_id}/articles'
    _url_post_recepcions = '/recepcions'
    _url_post_unitat_logistica = '/recepcions/{recepcio_id}/unitat_logistica'
    _url_post_finalitzar = '/recepcions/{recepcio_id}/finalitzar'

    def __init__(self, con: JManCon):
        self._con = con

    def list_proveidors(self):
        res = self._con.get(url=self._url_proveidors)
        return res.json()

    def get_proveidor(self, proveidor_id: int):
        res = self._con.get(url=self._url_proveidor.format(proveidor_id=str(proveidor_id)))
        return res.json()

    def get_articles(self, proveidor_id: int):
        res = self._con.get(url=self._url_proveidor_articles.format(proveidor_id=str(proveidor_id)))
        return res.json()

    def post_recepcio(self, recepcio: dict):
        res = self._con.post(url=self._url_post_recepcions, data=recepcio)
        return res.json()

    def post_unitat_logistica(self, recepcio_id: int,  unitat_logistica: dict):
        res = self._con.post(url=self._url_post_unitat_logistica.format(recepcio_id=recepcio_id), data=unitat_logistica)
        return res.json()

    def post_finalitzar(self, recepcio_id: int, dades_albara: dict):
        res = self._con.post(url=self._url_post_finalitzar.format(recepcio_id=recepcio_id), data=dades_albara)
        return res.json()
