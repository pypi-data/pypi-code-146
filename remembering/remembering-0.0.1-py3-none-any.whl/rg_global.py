NO_VALUE_SET_INT = -1
BREATHING_PHRASE_SEPARATOR = ";"

current_item_id_int = NO_VALUE_SET_INT


def resize_image(i_image_qlabel_ref, i_max_height):
    image_width_int = i_image_qlabel_ref.pixmap().width()
    image_height_int = i_image_qlabel_ref.pixmap().height()
    if image_width_int == 0:
        return
    height_relation_float = i_max_height / image_height_int

    new_height = i_max_height
    new_width = image_width_int * height_relation_float

    i_image_qlabel_ref.setFixedWidth(new_width)
    i_image_qlabel_ref.setFixedHeight(new_height)


def is_image_file(file_name_str):
    if (
            file_name_str.lower().endswith(".png") or
            file_name_str.lower().endswith(".jpg") or
            file_name_str.lower().endswith(".jpeg")
    ):
        return True
    return False


def filter_func(file_name_str):
    if file_name_str.lower().endswith(".png"):
        return True
    if file_name_str.lower().endswith(".jpg"):
        return True
    if file_name_str.lower().endswith(".jpeg"):
        return True
    return False


def is_text_file(file_name_str):
    if file_name_str.lower().endswith(".txt"):
        return True
    return False


def get_time_diff_string(i_old_time_ts: int, i_new_time_ts: int) -> str:
    diff_time_secs_int = abs(i_new_time_ts - i_old_time_ts)
    diff_time_mins_int = (diff_time_secs_int + 59) // 60
    if diff_time_mins_int >= 60:
        diff_time_hours_int = diff_time_mins_int // 60
        diff_time_str = str(diff_time_hours_int) + "h"
    else:
        diff_time_str = str(diff_time_mins_int) + "m"
    return diff_time_str
