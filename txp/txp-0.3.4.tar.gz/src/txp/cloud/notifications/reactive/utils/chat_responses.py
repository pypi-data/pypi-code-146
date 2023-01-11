from enum import Enum


class TwilioTemplates(Enum):
    """Twilio approved template models. Do not change this strings without approval."""

    ASSET_STATUS_SHORT = "El activo {} está actualmente en condición {}."
    SERVICE_NOT_AVAILABLE_CONTACT_US = "No tienes ese servicio contratado. Si quieres saber más, puedes contactar con nosotros."
    ASK_REPORT_ASSETS = "¿Deseas recibir un reporte de tus activos?"


class WhatsAppResponses(Enum):
    """Chat responses for WhatsApp."""

    ONLY_WORKS_ON_WHATSAPP = (
        "Solo puedo responder a eso si utilizas WhatsApp. Mis diculpas."
    )
    REPORT_SENT = "Aquí está el reporte."
    NOT_SUPPORTED_AT_THIS_TIME = (
        "Función no soportada por el momento. Pedimos disculpas."
    )
    ASSET_DATA_12_HR_NOT_FOUND = "No encuentro ese activo o datos sobre él en las últimas 12 horas. Intenta de nuevo con otro nombre o contacta con nuestro servicio técnico."


ASSET_NAMES = {
    "Showroom_Fridge": "frigorífico de exhibición",
}

CONDITION_NAMES = {
    "OPTIMAL": "óptima",
    "GOOD": "buena",
    "OPERATIONAL": "operativa",
    "CRITICAL": "crítica",
    "UNDEFINED": "desconocida",
}
