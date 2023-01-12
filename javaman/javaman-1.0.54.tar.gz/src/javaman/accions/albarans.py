from javaman.connexio import JManCon


class Albarans:
    __slots__ = '_con'

    _url_get_llistat_albarans = '/albarans'
    _url_get_albara_imprimir = '/albarans/{albara_id}/imprimir'

    def __init__(self, con: JManCon):
        self._con = con

    def get_albarans_imprimir(self, p_albara_id: int):
        req = self._con.get(url=self._url_get_albara_imprimir.format(albara_id=p_albara_id))
        return req.json()

    def get_albarans_llistat(self,
                           exercici: int = None,
                           client_id: int = None,
                           tercer_distribucio_id: int = None,
                           data_albara_inicial: str = None,
                           data_albara_final: str = None,
                           article_id: int = None,
                           article_atribut_id : int = None,
                           empleat_id : int = None,
                           repartidor_id: int = None,
                           article_lot_id : int = None,
                           article_lot: str = None
                             ):
        tmp_url = self._url_get_llistat_albarans
        tmp_params = []
        if exercici is not None:
            tmp_params.append("exercici="+str(exercici))
        if client_id is not None:
            tmp_params.append("client_id=" + str(client_id))
        if tercer_distribucio_id is not None:
            tmp_params.append("tercer_destinatari_id="+str(tercer_distribucio_id))
        if data_albara_inicial is not None:
            tmp_params.append("data_albara_inicial="+data_albara_inicial)
        if data_albara_final is not None:
            tmp_params.append("data_albara_final="+data_albara_final)
        if article_id is not None:
            tmp_params.append("article_id="+str(article_id))
        if article_atribut_id is not None:
            tmp_params.append("article_atribut_id="+str(article_atribut_id))
        if empleat_id is not None:
            tmp_params.append("empleat_id="+str(empleat_id))
        if repartidor_id is not None:
            tmp_params.append("repartidor_id="+str(repartidor_id))
        if article_lot_id is not None:
            tmp_params.append("article_lot_id="+str(article_lot_id))
        if article_lot is not None:
            tmp_params.append("article_lot="+article_lot)
        tmp_query = ""
        if len(tmp_params) > 0:
            tmp_query = "?"
            for xx in tmp_params:
                tmp_query += "&" + xx

        req = self._con.get(url=tmp_url + tmp_query)
        return req.json()
