from javaman.connexio import JManCon


class Factures:
    __slots__ = '_con'

    _url_get_llistat_factures = '/factures'
    _url_get_factures_imprimir = '/factures/{factura_id}/imprimir'

    def __init__(self, con: JManCon):
        self._con = con

    def get_factures_imprimir(self, p_factura_id: int):
        req = self._con.get(url=self._url_get_factures_imprimir.format(factura_id=p_factura_id))
        return req.json()

    def get_factures_llistat(self,
                           exercici: int = None,
                           client_id: int = None,
                           tercer_distribucio_id: int = None,
                           data_factura_inicial: str = None,
                           data_factura_final: str = None):
        tmp_url = self._url_get_llistat_factures
        tmp_params = []
        if exercici is not None:
            tmp_params.append("exercici=" + str(exercici))
        if client_id is not None:
            tmp_params.append("client_id=" + str(client_id))
        if tercer_distribucio_id is not None:
            tmp_params.append("tercer_destinatari_id=" + str(tercer_distribucio_id))
        if data_factura_inicial is not None:
            tmp_params.append("data_factura_inicial=" + data_factura_inicial)
        if data_factura_final is not None:
            tmp_params.append("data_factura_final=" + data_factura_final)
        tmp_query = ""
        if len(tmp_params) > 0:
            tmp_query = "?"
            for xx in tmp_params:
                tmp_query += "&" + xx

        req = self._con.get(url=tmp_url + tmp_query)
        return req.json()
