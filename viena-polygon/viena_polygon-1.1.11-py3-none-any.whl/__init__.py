# polygon/__init__.py

__app_name__ = "polygon"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    CONNECT_ERROR,
    SERVER_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    CONNECT_ERROR: "connect error",
    SERVER_ERROR: "server error",
    ID_ERROR: "id error",
}
