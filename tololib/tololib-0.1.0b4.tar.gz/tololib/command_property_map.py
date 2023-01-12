from .command import Command

SET_STATUS_COMMAND_PROPERTY_MAP = {
    Command.SET_POWER_ON: "power_on",
    Command.SET_FAN_ON: "fan_on",
    Command.SET_AROMA_THERAPY_ON: "aroma_therapy_on",
    Command.SET_LAMP_ON: "lamp_on",
    Command.SET_SWEEP_ON: "sweep_on",
    Command.SET_SALT_BATH_ON: "salt_bath_on",
}

GET_STATUS_COMMAND_PROPERTY_MAP = {
    Command.GET_FAN_TIMER: "fan_timer",
    Command.GET_SALT_BATH_TIMER: "salt_bath_timer",
}

SET_SETTINGS_COMMAND_PROPERTY_MAP = {
    Command.SET_TARGET_TEMPERATURE: "target_temperature",
    Command.SET_TARGET_HUMIDITY: "target_humidity",
    Command.SET_POWER_TIMER: "power_timer",
    Command.SET_SALT_BATH_TIMER: "salt_bath_timer",
    Command.SET_AROMA_THERAPY: "aroma_therapy",
    Command.SET_SWEEP_TIMER: "sweep_timer",
    Command.SET_LAMP_MODE: "lamp_mode",
    Command.SET_FAN_TIMER: "fan_timer",
}

GET_SETTINGS_COMMAND_PROPERTY_MAP = {
    Command.GET_LAMP_MODE: "lamp_mode",
    Command.GET_AROMA_THERAPY: "aroma_therapy",
}
