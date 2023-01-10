# -#- coding: utf-8 -#-
from facturacion_electronica import facturacion_electronica as fe
from facturacion_electronica.firma import Firma
import json
from lxml import etree
import unittest


class TestEjemploRespuestasComerciales(unittest.TestCase):
    """
    Test Ejemplo Respuestas Comerciales
    """
    def test_respuesta_recepcion(self):
        """
        Test Ejemplo Respuesta Recepción XML
        """
        print("Se inicia test Respuesta Recepción XML")
        f = open("facturacion_electronica/ejemplos/ejemplo_recepcion_dte.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.recepcion_xml(ejemplo)
        """
            Verifico Integridad XML
        """
        self.assertEqual(len(result), 1)
        print(result)
        for r in result:
            self.assertFalse(r.get('error', False))
            xml = etree.fromstring(
                r['respuesta_xml'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                                 '').encode('ISO-8859-1'))
            query = "Resultado/Caratula/RutResponde"
            self.assertEqual(xml.find(query).text, "16291998-9")
            query = "Resultado/Caratula/RutRecibe"
            self.assertEqual(xml.find(query).text, "88888888-8")
            query = "Resultado/RecepcionEnvio"
            RecepcionEnvio = xml.findall(query)
            self.assertEqual(len(RecepcionEnvio), 1)
            self.assertEqual(RecepcionEnvio[0].find('RutEmisor').text, "88888888-8")
            self.assertEqual(RecepcionEnvio[0].find('RutReceptor').text, "76289111-5")
            self.assertEqual(RecepcionEnvio[0].find('EstadoRecepEnv').text, "0")
            self.assertEqual(RecepcionEnvio[0].find('NroDTE').text, "2")
            query = "RecepcionDTE"
            RecepcionDTE = RecepcionEnvio[0].findall(query)
            self.assertEqual(len(RecepcionDTE), 2)
            self.assertEqual(RecepcionDTE[0].find('TipoDTE').text, "33")
            self.assertEqual(RecepcionDTE[0].find('RUTEmisor').text, "88888888-8")
            self.assertEqual(RecepcionDTE[0].find('RUTRecepr').text, "76289111-5")
            self.assertEqual(RecepcionDTE[0].find('EstadoRecepEnv').text, "3")
            self.assertEqual(RecepcionDTE[1].find('TipoDTE').text, "33")
            self.assertEqual(RecepcionDTE[1].find('RutEmisor').text, "88888888-8")
            self.assertEqual(RecepcionDTE[1].find('RutReceptor').text, "76289111-5")
            self.assertEqual(RecepcionDTE[1].find('EstadoRecepEnv').text, "0")

    """
    Test Resuesta Recepción Mercaderías
    """
    def test_respuesta_rececpion_mercaderias(self):
        """
        Test Ejemplo Reenvío Correo de Envío
        """
        print("Se inicia test Reenvío Correo de Envío")
        f = open("facturacion_electronica/ejemplos/ejemplo_validacion_mercaderias.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.recepcion_mercaderias(ejemplo)
        self.assertFalse(result.get('error', False))
        """
            Verifico Integridad XML
        """
        self.assertFalse(result.get('errores', False))
        xml = etree.fromstring(
            result['respuesta_xml'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
        print(xml)
        query = "SetRecibos/Caratula/RutResponde"
        self.assertEqual(xml.find(query).text, "16291998-9")
        query = "SetRecibos/Caratula/RutRecibe"
        self.assertEqual(xml.find(query).text, "88888888-8")
        query = "Recibo"
        Receibo = xml.findall(query)
        self.assertEqual(len(Recibo), 2)
        query = "DocumentoRecibo"
        DocumentoRecibo = Recibo[0].find(query)
        self.assertEqual(Recibo.find('TipoDoc').text, "33")
        self.assertEqual(Recibo.find('Folio').text, "14")
        self.assertEqual(Recibo.find('RutEmisor').text, "88888888-8")
        self.assertEqual(Recibo.find('RutReceptor').text, "76289111-5")
        self.assertEqual(Recibo.find('EstadoRecepEnv').text, "3")
        self.assertIsNotNone(Recibo.find('Declaracion'))
        DocumentoRecibo = Recibo[1].find(query)
        self.assertEqual(Recibo.find('TipoDTE').text, "33")
        self.assertEqual(Recibo.find('Folio').text, "15")
        self.assertEqual(Recibo.find('RutEmisor').text, "88888888-8")
        self.assertEqual(Recibo.find('RutReceptor').text, "76289111-5")
        self.assertEqual(Recibo.find('EstadoRecepEnv').text, "0")
        self.assertIsNotNone(Recibo.find('Declaracion'))

    def test_respuesta_rececpion_comercial(self):
        """
        Test Ejemplo Respuesta Recepción Comercial
        """
        print("Se inicia test Respuesta Recepción Comercial")
        f = open("facturacion_electronica/ejemplos/ejemplo_validacion_comercial.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.validacion_comercial(ejemplo)
        self.assertFalse(result.get('errores', False))
        self.assertFalse(result.get('errores', False))
        """
            Verifico Integridad XML
        """
        self.assertFalse(result.get('errores', False))
        xml = etree.fromstring(
            result['respuesta_xml'].replace('xmlns="http://www.sii.cl/SiiDte"',
                                             '').encode('ISO-8859-1'))
        query = "Resultado/Caratula/RutResponde"
        self.assertEqual(xml.find(query).text, "16291998-9")
        query = "Resultado/Caratula/RutRecibe"
        self.assertEqual(xml.find(query).text, "88888888-8")
        query = "Resultado/ResultadoDTE"
        ResultadoDTE = xml.findall(query)
        self.assertEqual(len(ResultadoDTE), 2)
        self.assertEqual(ResultadoDTE[0].find('TipoDTE').text, "33")
        self.assertEqual(ResultadoDTE[0].find('Folio').text, "14")
        self.assertEqual(ResultadoDTE[0].find('RutEmisor').text, "88888888-8")
        self.assertEqual(ResultadoDTE[0].find('RutRecep').text, "76289111-5")
        self.assertEqual(ResultadoDTE[0].find('EstadoDTE').text, "0")
        self.assertIsNone(ResultadoDTE[0].find('CodRchDsc'))
        self.assertEqual(ResultadoDTE[1].find('TipoDTE').text, "33")
        self.assertEqual(ResultadoDTE[1].find('Folio').text, "15")
        self.assertEqual(ResultadoDTE[1].find('RutEmisor').text, "88888888-8")
        self.assertEqual(ResultadoDTE[1].find('RutReceptor').text, "76289111-5")
        self.assertEqual(ResultadoDTE[1].find('EstadoDTE').text, "2")
        self.assertEqual(ResultadoDTE[1].find('CodRchDsc'), "-1")


if __name__ == '__main__':
    unittest.main()
