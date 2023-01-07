import dataclasses
import json
import logging
import os

import matc.gui
import matc.shared

"""
Contains state for the application, which is mostly contained in the settings dict, which is stored
in a json file between application restarts. The state not stored between restarts can be seen just
below here

The initiation function init_state must be called before using the values here. We need this
approach because ___________
"""
ACTIVE_PHRASE_NOT_SET: int = -1
active_phrase_id: int = ACTIVE_PHRASE_NOT_SET

JSON_OBJ_TYPE = "__obj_type__"

# Setting Keys (SK)
SK_MASTER_VOLUME = "master_volume"
SK_BREATHING_AUDIO_VOLUME = "breathing_audio_volume"
SK_BREATHING_AUDIO_FILE_PATH = "breathing_audio_file_path"
SK_NOTIFICATION_AUDIO_VOLUME = "notification_audio_volume"
SK_NOTIFICATION_AUDIO_FILE_PATH = "notification_audio_file_path"
SK_BREATHING_BREAK_TIMER_SECS = "breathing_break_timer_secs"
SK_BREATHING_PHRASES = "breathing_phrases"
SK_BREATHING_VISUALIZATION = "breathing_visualization"
SK_MOVE_MOUSE_CURSOR = "move_mouse_cursor"
SK_NOTIFICATION_DURATION_MSECS = "notification_duration_msecs"

default_breathing_audio_file_path = matc.shared.get_audio_path("big_bell[cc0]_fade_out.wav")
default_notification_audio_file_path = matc.shared.get_audio_path("small_bell_short[cc0].wav")

BREATHING_BREAK_TIMER_DEFAULT_SECS = 60 * 10
NOTIFICATION_DURATION_DEFAULT_MSECS = 8 * 1000
MASTER_VOLUME_DEFAULT = 40
BREATHING_AUDIO_VOLUME_DEFAULT = 40
NOTIFICATION_AUDIO_VOLUME_DEFAULT = 40
BREATHING_VISUALIZATION_DEFAULT = matc.shared.BrVis.bar.value

settings_file_path = ""
settings: dict = {}
settings_base: dict = {
    SK_MASTER_VOLUME: MASTER_VOLUME_DEFAULT,
    SK_BREATHING_AUDIO_VOLUME: BREATHING_AUDIO_VOLUME_DEFAULT,
    SK_NOTIFICATION_AUDIO_VOLUME: NOTIFICATION_AUDIO_VOLUME_DEFAULT,
    SK_BREATHING_AUDIO_FILE_PATH: default_breathing_audio_file_path,
    SK_NOTIFICATION_AUDIO_FILE_PATH: default_notification_audio_file_path,
    SK_NOTIFICATION_DURATION_MSECS: NOTIFICATION_DURATION_DEFAULT_MSECS,
    SK_BREATHING_BREAK_TIMER_SECS: BREATHING_BREAK_TIMER_DEFAULT_SECS,
    SK_BREATHING_PHRASES: [],
    SK_BREATHING_VISUALIZATION: BREATHING_VISUALIZATION_DEFAULT,
    SK_MOVE_MOUSE_CURSOR: True,
}


@dataclasses.dataclass
class SettingsListObject:
    id: int


@dataclasses.dataclass
class BreathingPhrase(SettingsListObject):
    """
    To update we can use the get function and then just modify the object
    """
    in_breath: str
    out_breath: str


def _get_list_object(settings_key: str, i_obj_id: int):
    # -> SettingsListObject
    list_objects: list = settings[settings_key]
    for o in list_objects:
        if o.id == i_obj_id:
            return o
    topmost = get_topmost_breathing_phrase()
    return topmost
    # raise Exception(f"No list object found in the list {file_path_settings_key} for the id {
    # i_obj_id}")


def get_breathing_phrase(i_id: int) -> BreathingPhrase:
    return _get_list_object(SK_BREATHING_PHRASES, i_id)


def get_topmost_breathing_phrase() -> BreathingPhrase:
    list_objects: list = settings[SK_BREATHING_PHRASES]
    if len(list_objects) < 1:
        raise Exception("List is empty, so cannot return item")
    return list_objects[0]


def _add_list_object(i_settings_key: str, i_class, *args) -> int:
    """
    The order of JSON arrays are preserved (and of course Python lists too)
    https://stackoverflow.com/a/7214312/2525237
    """
    list_objects: list = settings[i_settings_key]  # -reference
    highest_id: int = 0
    if list_objects:
        highest_id: int = max(lo.id for lo in list_objects)
    new_id: int = highest_id + 1
    new_br_phrase = i_class(new_id, *args)
    list_objects.append(new_br_phrase)
    return new_id


def add_breathing_phrase(i_in_breath: str, i_out_breath: str) -> int:
    new_id = _add_list_object(SK_BREATHING_PHRASES, BreathingPhrase, i_in_breath, i_out_breath)
    return new_id


def _remove_list_object(i_settings_key: str, i_id: int) -> None:
    list_objects: list = settings[i_settings_key]
    for o in list_objects:
        if o.id == i_id:
            list_objects.remove(o)
            return
    raise Exception("Could not find object in list")


def remove_breathing_phrase(i_id: int):
    _remove_list_object(SK_BREATHING_PHRASES, i_id)


########################


class MyEncoder(json.JSONEncoder):
    def default(self, obj):  # -overridden
        if issubclass(type(obj), SettingsListObject):
            object_dictionary: dict = obj.__dict__
            type_value = type(obj).__name__
            # if isinstance(obj, BreathingPhrase):
            # type_value = BreathingPhrase.__name__
            # else: raise Exception(f"Cannot endode object: Case is not covered")
            object_dictionary[JSON_OBJ_TYPE] = type_value
            return obj.__dict__
        return super().default(obj)


def my_decode(dct: dict):
    """
    From the documentation: "object_hook is an optional function that will be called with the
    result of any object literal decoded (a dict). The return value of object_hook will be used
    instead of the dict."
    """
    if JSON_OBJ_TYPE in dct and dct[JSON_OBJ_TYPE] == BreathingPhrase.__name__:
        breathing_phrase_obj = BreathingPhrase(
            id=dct["id"],
            in_breath=dct["in_breath"],
            out_breath=dct["out_breath"]
        )
        return breathing_phrase_obj
    return dct


def settings_file_exists() -> bool:
    return os.path.isfile(settings_file_path)


"""
def backup_settings_file() -> None:
    if matc.shared.testing_bool:
        return
    date_sg = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name = matc.shared.get_settings_file_path(date_sg)
    shutil.copyfile(settings_file_path, new_file_name)
    # Removing older backups
    # Checking if it's well-formatted (JSON ok?)
"""


def is_json_file_valid(i_path: str) -> bool:
    with open(i_path, "r") as f:
        try:
            json.load(f)
        except ValueError:
            logging.error("Invalid json")
            return False
    return True


def save_settings_to_json_file():
    # logging.debug(f"Saving to json file. {matc.state.settings=}")
    logging.debug("Saving to json file")
    if not settings_file_path:
        logging.error("No settings file specified - cannot save")
        return
    temp_settings_file_path = os.path.join(os.path.dirname(settings_file_path),
        "temporary-save-file.json")
    if os.path.exists(temp_settings_file_path):
        os.remove(temp_settings_file_path)
    with open(temp_settings_file_path, "w") as write_file:
        json.dump(matc.state.settings, write_file, indent=2, cls=MyEncoder)
    if not is_json_file_valid(temp_settings_file_path):
        logging.error("JSON file to be written is not valid. Data has not been written.")
        return
    if os.path.exists(settings_file_path):
        os.remove(settings_file_path)
    os.rename(temp_settings_file_path, settings_file_path)
    # -Overwriting the original file. (Renaming is atomic).


def _initiate_settings_dict():
    """with json data from file"""
    global settings
    settings = settings_base.copy()

    if not settings_file_exists():
        # min_settings_dict[SK_REST_ACTIONS].update(init_rest_actions)
        add_breathing_phrase(
            "Breathing in I know I am breathing in",
            "Breathing out I know I am breathing out"
        )
        add_breathing_phrase(
            "Breathing in I follow the whole length of my in-breath",
            "Breathing out I follow the whole length of my out-breath"
        )
        add_breathing_phrase(
            "Breathing in I am aware of my body",
            "Breathing out I am aware of my body"
        )
        add_breathing_phrase(
            "May everyone live with compassion",
            "May everyone live in peace"
        )
        add_breathing_phrase(
            "Breathing in I know I am what I am doing at the computer",
            "Breathing out I am aware of my connection with other people"
        )
        """
        Aware of stress in me ("Taking a breather")
        Breathing out I am aware of how my actions help others
        "Breathing in, I care for my body","Breathing out, I relax my body",
        "Happy, At Peace","May I be happy",
        "Breathing in I share the well-being of others","Breathing out I contribute to the
        well-being
        of others",
        "Breathing in compassion to myself","Breathing out compassion to others",
        "Self-love and acceptance","I love and accept myself just as I am",
        "Sitting at the computer"
        """

    if not os.path.isfile(settings_file_path):
        return
    with open(settings_file_path, "r") as read_file:
        try:
            from_file_dict: dict = json.load(read_file, object_hook=my_decode)
        except json.decoder.JSONDecodeError:
            matc.gui.modal_dialogs.ErrorDlg.log_and_start(logging.error, "JSONDecodeError")
            return

    diff_key_list: list = []
    for min_key in settings.keys():
        if min_key not in from_file_dict.keys():
            diff_key_list.append(min_key)
    if diff_key_list:
        # diff_keys_str = ", ".join(diff_key_list)
        logging.info(
            "One or more keys needed for the application to work were not "
            f"available in {os.path.basename(settings_file_path)} so have been added now "
            f"(with a default value). These are the keys: {diff_key_list}")

    diff_key_list: list = []
    for file_key in from_file_dict.keys():
        if file_key not in settings.keys():
            diff_key_list.append(file_key)
    if diff_key_list:
        # diff_keys_str = ", ".join(diff_key_list)
        logging.info(
            f"One or more keys in {os.path.basename(settings_file_path)} are not used by the "
            "application. This is probably because they have been used before and are now "
            f"deprecated. These are the keys: {diff_key_list}")

    settings.update(from_file_dict)
    # -if there are different values for one key, the value in from_file_dict takes precendence


def initiate_state(i_settings_file_path: str):
    dir_ = os.path.dirname(i_settings_file_path)

    global settings_file_path
    if dir_ and os.path.isdir(dir_):
        settings_file_path = i_settings_file_path
    else:
        raise Exception("Settings path is not valid")

    _initiate_settings_dict()

    global active_phrase_id
    first_bp = get_topmost_breathing_phrase()
    active_phrase_id = first_bp.id
