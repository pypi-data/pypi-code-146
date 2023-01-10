from lxml import etree

from correos_preregistro.requests.preregistro_envio import (
    RequestPreregistroEnvio,
    RequestPreregistroEnvioDestinatario,
    RequestPreregistroEnvioEnvio,
    RequestPreregistroEnvioRemitente,
)
from correos_preregistro.responses.preregistro_envio import CustomResponse


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
        ).filled_xml
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
        return CustomResponse(
            shipment_code,
            label_file,
        )

    def _destinatario(receiver):
        return RequestPreregistroEnvioDestinatario.xml.format(
            nombre=receiver.name,
            apellidos=receiver.surname,
            direccion=receiver.address,
            localidad=receiver.city,
            provincia=receiver.state,
            cp=receiver.zip,
            telefono=receiver.phone,
            email=receiver.email,
            telefono_sms=receiver.phone,
            idioma_sms=1 if receiver.lang == "ES" else 2,
        )

    def _remitente(sender):
        return RequestPreregistroEnvioRemitente.xml.format(
            nombre=sender.name,
            nif=sender.surname,
            direccion=sender.address,
            localidad=sender.city,
            provincia=sender.state,
            cp=sender.zip,
            telefono=sender.phone,
            email=sender.email,
        )

    def _envio(package):
        return RequestPreregistroEnvioEnvio.xml.format(
            cod_producto=package.product_code,
            tipo_franqueo=package.postage_type,
            modalidad_entrega=package.delivery_modality,
            tipo_peso=package.weight_type,
            peso=package.weight,
        )
