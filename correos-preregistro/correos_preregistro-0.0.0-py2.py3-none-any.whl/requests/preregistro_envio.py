from datetime import datetime


class RequestPreregistroEnvioIdentificacion:
    raw_xml = """
    <Identificacion>
      <Nombre>{nombre}</Nombre>
      <Apellido1>{apellidos}</Apellido1>
    </Identificacion>
    """
    raw_xml_with_nif = """
    <Identificacion>
      <Nombre>{nombre}</Nombre>
      <Nif>{nif}</Nif>
    </Identificacion>
    """

    def __init__(self, nombre, apellidos=None, nif=None):
        if nif:
            self.xml = self.raw_xml_with_nif.format(
                nombre=nombre,
                nif=nif,
            )
        else:
            self.xml = self.raw_xml.format(
                nombre=nombre,
                apellidos=apellidos,
            )


class RequestPreregistroEnvioDatosDireccion:
    raw_xml = """
    <DatosDireccion>
      <Direccion>{direccion}</Direccion>
      <Localidad>{localidad}</Localidad>
      <Provincia>{provincia}</Provincia>
    </DatosDireccion>
    """

    def __init__(self, direccion, localidad, provincia):
        self.xml = self.raw_xml.format(
            direccion=direccion,
            localidad=localidad,
            provincia=provincia,
        )


class RequestPreregistroEnvioRemitente:
    raw_xml = """
    <Remitente>
      {identificacion}
      {direccion}
      <CP>{cp}</CP>
      <Telefonocontacto>{telefono}</Telefonocontacto>
      <Email>{email}</Email>
      <DatosSMS>
        <NumeroSMS/>
        <Idioma/>
      </DatosSMS>
    </Remitente>
    """

    def __init__(self, identificacion, direccion, cp, telefono, email):
        self.xml = self.raw_xml.format(
            identificacion=identificacion,
            direccion=direccion,
            cp=cp,
            telefono=telefono,
            email=email,
        )


class RequestPreregistroEnvioDestinatario:
    raw_xml = """
    <Destinatario>
      {identificacion}
      {direccion}
      <CP>{cp}</CP>
      <Telefonocontacto>{telefono}</Telefonocontacto>
      <Email>{email}</Email>
      <DatosSMS>
        <NumeroSMS>{telefono_sms}</NumeroSMS>
        <Idioma>{idioma_sms}</Idioma>
      </DatosSMS>
    </Destinatario>
    """

    def __init__(
        self, identificacion, direccion, cp, telefono, email, telefono_sms, idioma_sms
    ):
        self.xml = self.raw_xml.format(
            identificacion=identificacion,
            direccion=direccion,
            cp=cp,
            telefono=telefono,
            email=email,
            telefono_sms=telefono_sms,
            idioma_sms=idioma_sms,
        )


class RequestPreregistroEnvioEnvio:
    raw_xml = """
    <Envio>
      <CodProducto>{cod_producto}</CodProducto>
      <ModalidadEntrega>{modalidad_entrega}</ModalidadEntrega>
      <TipoFranqueo>{tipo_franqueo}</TipoFranqueo>
      <Pesos>
        <Peso>
          <TipoPeso>{tipo_peso}</TipoPeso>
          <Valor>{peso}</Valor>
        </Peso>
      </Pesos>
    </Envio>
    """

    def __init__(self, cod_producto, modalidad_entrega, tipo_franqueo, tipo_peso, peso):
        self.xml = self.raw_xml.format(
            cod_producto=cod_producto,
            modalidad_entrega=modalidad_entrega,
            tipo_franqueo=tipo_franqueo,
            tipo_peso=tipo_peso,
            peso=peso,
        )


class RequestPreregistroEnvio:
    raw_xml = """
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
      {Remitente}
      {Destinatario}
      {Envio}
    </PreregistroEnvio>
  </soapenv:Body>
</soapenv:Envelope>
"""

    def __init__(self, codigo_etiquetador, destinatario, remitente, envio):
        # 23-01-2011 10:54:12
        DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
        self.xml = self.raw_xml.format(
            FechaOperacion=datetime.now().strftime(DATE_FORMAT),
            CodEtiquetador=codigo_etiquetador,
            Remitente=remitente,
            Destinatario=destinatario,
            Envio=envio,
        ).encode("utf8")
