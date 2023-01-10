from datetime import datetime


class RequestPreregistroEnvioRemitente:
    xml = """
    <Identificacion>
      <Nombre>{nombre}</Nombre>
      <Nif>{nif}</Nif>
    </Identificacion>
    <DatosDireccion>
      <Direccion>{direccion}</Direccion>
      <Localidad>{localidad}</Localidad>
      <Provincia>{provincia}</Provincia>
    </DatosDireccion>
    <CP>{cp}</CP>
    <Telefonocontacto>{telefono}</Telefonocontacto>
    <Email>{email}</Email>
    <DatosSMS>
      <NumeroSMS/>
      <Idioma/>
    </DatosSMS>
    """


class RequestPreregistroEnvioDestinatario:
    xml = """
    <!-- PARTNER  -->
    <Identificacion>
      <Nombre>{nombre}</Nombre>
      <Apellido1>{apellidos}</Apellido1>
    </Identificacion>
    <DatosDireccion>
      <!-- DIRECCIÓ ENVIAMENT PARTNER  -->
      <Direccion>{direccion}</Direccion>
      <Localidad>{localidad}</Localidad>
      <Provincia>{provincia}</Provincia>
    </DatosDireccion>
    <CP>{cp}</CP>
    <Telefonocontacto>{telefono}</Telefonocontacto>
    <Email>{email}</Email>
    <DatosSMS>
      <NumeroSMS>{telefono_sms}</NumeroSMS>
      <Idioma>{idioma_sms}</Idioma>
    </DatosSMS>
    """


class RequestPreregistroEnvioEnvio:
    xml = """
    <CodProducto>{cod_producto}</CodProducto>
    <ModalidadEntrega>{modalidad_entrega}</ModalidadEntrega>
    <TipoFranqueo>{tipo_franqueo}</TipoFranqueo>
    <Pesos>
      <Peso>
        <TipoPeso>{tipo_peso}</TipoPeso>
        <Valor>{peso}</Valor>
      </Peso>
    </Pesos>
    """


class RequestPreregistroEnvio:
    xml = """
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns="http://www.correos.es/iris6/services/preregistroetiquetas">
  <soapenv:Header/>
  <soapenv:Body>
    <PreregistroEnvio>
      <IdiomaErrores/>
      <FechaOperacion>{FechaOperacion}</FechaOperacion>
      <CodEtiquetador>{CodEtiquetador}</CodEtiquetador>
      <ModDevEtiqueta>2</ModDevEtiqueta>
      <Remitente>
        {Remitente}
      </Remitente>
      <Destinatario>
        {Destinatario}
      </Destinatario>
      <Envio>
        {Envio}
      </Envio>
    </PreregistroEnvio>
  </soapenv:Body>
</soapenv:Envelope>
"""

    def __init__(self, codigo_etiquetador, destinatario, remitente, envio):
        # 23-01-2011 10:54:12
        DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
        self.filled_xml = self.xml.format(
            FechaOperacion=datetime.now().strftime(DATE_FORMAT),
            CodEtiquetador=codigo_etiquetador,
            Remitente=remitente,
            Destinatario=destinatario,
            Envio=envio,
        ).encode("utf8")
