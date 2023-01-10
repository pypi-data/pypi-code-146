from lxml import etree

from correos_preregistro.requests.preregistro_envio import (
    RequestPreregistroEnvio,
    RequestPreregistroEnvioDatosDireccion,
    RequestPreregistroEnvioDestinatario,
    RequestPreregistroEnvioEnvio,
    RequestPreregistroEnvioIdentificacion,
    RequestPreregistroEnvioRemitente,
)
from correos_preregistro.responses.preregistro_envio import ResponsePreregistroEnvio


class PreRegistrationShipment:
    @classmethod
    def create(cls, client, code, receiver, sender, package):
        xml_destinatario = cls._destinatario(receiver)
        xml_remitente = cls._remitente(sender)
        xml_envio = cls._envio(package)

        request = RequestPreregistroEnvio(
            codigo_etiquetador=code,
            destinatario=xml_destinatario,
            remitente=xml_remitente,
            envio=xml_envio,
        ).xml
        response = client.send_request(payload=request)
        # TODO: Why???
        # shipment_code = root.xpath(".//CodEnvio")
        # label_file = root.xpath(".//Fichero")
        root = etree.fromstring(response)
        shipment_code = (
            root.getchildren()[1]
            .getchildren()[0]
            .getchildren()[-1]
            .getchildren()[1]
            .text
        )
        label_file = (
            root.getchildren()[1]
            .getchildren()[0]
            .getchildren()[-1]
            .getchildren()[-1]
            .getchildren()[-1]
            .getchildren()[-1]
            .text
        )
        return ResponsePreregistroEnvio(
            shipment_code,
            label_file,
        )

    def _destinatario(receiver):
        xml_identificacion = RequestPreregistroEnvioIdentificacion(
            nombre=receiver.name,
            apellidos=receiver.surname,
        ).xml
        xml_direccion = RequestPreregistroEnvioDatosDireccion(
            direccion=receiver.address,
            localidad=receiver.city,
            provincia=receiver.state,
        ).xml
        return RequestPreregistroEnvioDestinatario(
            identificacion=xml_identificacion,
            direccion=xml_direccion,
            cp=receiver.zip,
            telefono=receiver.phone,
            email=receiver.email,
            telefono_sms=receiver.phone,
            idioma_sms=1 if receiver.lang == "ES" else 2,
        ).xml

    def _remitente(sender):
        xml_identificacion = RequestPreregistroEnvioIdentificacion(
            nombre=sender.name,
            nif=sender.nif,
        ).xml
        xml_direccion = RequestPreregistroEnvioDatosDireccion(
            direccion=sender.address,
            localidad=sender.city,
            provincia=sender.state,
        ).xml
        return RequestPreregistroEnvioRemitente(
            identificacion=xml_identificacion,
            direccion=xml_direccion,
            cp=sender.zip,
            telefono=sender.phone,
            email=sender.email,
        ).xml

    def _envio(package):
        return RequestPreregistroEnvioEnvio(
            cod_producto=package.product_code,
            modalidad_entrega=package.delivery_modality,
            tipo_franqueo=package.postage_type,
            tipo_peso=package.weight_type,
            peso=package.weight,
        ).xml
