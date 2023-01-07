from typing import Union, Optional, Literal, TypedDict
import subprocess
import tempfile
import locale
import os
import re


__version__ = "2.2"
"The version"


def _compare_dict(first_dict: dict, second_dict: dict) -> bool:
    if len(first_dict) != len(second_dict):
        return False

    for key, value in first_dict.items():
        if key not in second_dict:
            return False

        if value != second_dict[key]:
            return False

    return True


def _strip_list(old_list: list[str]) -> list[str]:
    new_list = []
    for i in old_list:
        new_list.append(i.strip())
    return new_list


def _parse_desktop_sections(content: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    current_section = None
    for line in content.splitlines():
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            sections[current_section] = {}
        elif current_section is None:
            continue
        else:
            try:
                key, value = line.split("=", 1)
                sections[current_section][key] = value
            except ValueError:
                continue
    return sections


def _string_to_bool(string: Optional[str]) -> Optional[bool]:
    "Converts a String to a Boolean"
    if string is None:
        return None
    elif string.lower() == "true":
        return True
    elif string.lower() == "false":
        return False
    else:
        return None


def _is_flatpak() -> bool:
    "Cheks if the lib is running inside a Flatpak"
    return os.path.isfile("/.flatpak-info")


def get_xdg_data_dirs() -> list[str]:
    "Get all XDG DATA DIRS"
    try:
        data_dirs = os.getenv("XDG_DATA_DIRS").split(":")
    except AttributeError:
        data_dirs = [os.path.expanduser("~/.local/share"), "/usr/share"]

    if _is_flatpak():
        return data_dirs + ["/run/host/usr/share"]
    else:
        return data_dirs


def _get_icon_size_dirs(path: str) -> list[str]:
    size_list = []
    for i in os.listdir(path):
        if not os.path.isdir(os.path.join(path, i)) or not re.match(r"\d+x\d+", i):
            continue

        size_list.append(int(re.search(r"^\d+", i).group()))

    size_list.sort(reverse=True)

    dir_list = []
    for i in size_list:
        dir_list.append(f"{i}x{i}")

    return dir_list


def get_icon_path(icon_name: str) -> Optional[str]:
    "Get the path of a Icon"
    for data_dir in get_xdg_data_dirs():
        scalable_dir = os.path.join(data_dir, "icons", "hicolor", "scalable")
        if os.path.isdir(scalable_dir):
            for directory in os.listdir(scalable_dir):
                icon_path = os.path.join(scalable_dir, directory, icon_name + ".svg")
                if os.path.isfile(icon_path):
                    return icon_path
        if os.path.isdir(os.path.join(data_dir, "icons", "hicolor")):
            for size in _get_icon_size_dirs(os.path.join(data_dir, "icons", "hicolor")):
                size_dir = os.path.join(data_dir, "icons", "hicolor", size)
                for directory in os.listdir(size_dir):
                    icon_path = os.path.join(size_dir, directory, icon_name + ".png")
                    if os.path.isfile(icon_path):
                        return icon_path
        if os.path.isdir(os.path.join(data_dir, "pixmaps")):
            if os.path.isfile(os.path.join(data_dir, "pixmaps", icon_name + ".png")):
                return os.path.join(data_dir, "pixmaps", icon_name + ".png")

    return None


class ValidationMessageDict(TypedDict):
    Error: list[str]
    FutureError: list[str]
    Warning: list[str]
    Hint: list[str]


class TranslatableKey:
    def __init__(self) -> None:
        self.default_text: str = ""
        "The untranslated text"

        self.translations: dict[str, str] = {}
        "The translations"

    def get_translated_text(self) -> str:
        "Returns the text for the current language"
        current_lang = locale.getlocale()[0]
        if current_lang is None:
            return self.default_text
        elif current_lang in self.translations:
            return self.translations[current_lang]
        elif current_lang.split("_")[0] in self.translations:
            return self.translations[current_lang.split("_")[0]]
        else:
            return self.default_text

    def load_section(self, section: dict[str, str], search_key: str) -> None:
        self.clear()

        for key, value in section.items():
            if not key.startswith(search_key):
                continue

            if search_key == key:
                self.default_text = value
            else:
                try:
                    lang = re.search(r"(?<=\[).+(?=\]$)", key).group()
                    self.translations[lang] = value
                except AttributeError:
                    continue

    def get_text(self, entry_key) -> str:
        if self.default_text == "":
            return ""

        text = f"{entry_key}={self.default_text}\n"
        for key, value in self.translations.items():
            text += f"{entry_key}[{key}]={value}\n"
        return text

    def clear(self) -> None:
        "Clear"
        self.default_text = ""
        self.translations.clear()

    def __repr__(self) -> str:
        return f"<TranslatableKey default_text='{self.default_text}'>"

    def __str__(self) -> str:
        return self.default_text

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, TranslatableKey):
            return False

        return self.default_text == obj.default_text and _compare_dict(self.translations, obj.translations)


class TranslatableListKey:
    def __init__(self) -> None:
        self.default_list: list[str] = []
        self.translations: dict[str, list[str]] = {}

    def load_section(self, section: dict[str, str], search_key: str) -> None:
        self.clear()

        for key, value in section.items():
            if not key.startswith(search_key):
                continue

            if search_key == key:
                self.default_text = value.removesuffix(";").split(";")
            else:
                try:
                    lang = re.search(r"(?<=\[).+(?=\]$)", key).group()
                    self.translations[lang] = value.removesuffix(";").split(";")
                except AttributeError:
                    continue

    def get_text(self, entry_key) -> str:
        if len(self.default_list) == 0:
            return ""

        text = f"{entry_key}={';'.join(self.default_text)};\n"
        for key, value in self.translations.items():
            text += f"{entry_key}[{key}]={';'.join(value)};\n"
        return text

    def clear(self) -> None:
        self.default_list.clear()
        self.translations.clear()

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, TranslatableListKey):
            return False

        return self.default_list == obj.default_list and _compare_dict(self.translations, obj.translations)


class DesktopAction:
    def __init__(self) -> None:
        self.Name: TranslatableKey = TranslatableKey()
        "The Name Key"

        self.Icon: Optional[str] = None
        "The Icon Key"

        self.Exec: Optional[str] = None
        "The Exec Key"

    @classmethod
    def from_dict(cls, action_section: dict[str, str]):
        "Load the Action from a Dict. Onyl used internaly."
        action = cls()

        action.Name.load_section(action_section, "Name")
        action.Icon = action_section.get("Icon", None)
        action.Exec = action_section.get("Exec", None)

        return action

    def get_text(self) -> str:
        "Converts the Action into a String"
        text = self.Name.get_text("Name")

        if self.Icon is not None:
            text += f"Icon={self.Icon}\n"

        if self.Exec is not None:
            text += f"Exec={self.Exec}"

        return text

    def get_icon_path(self) -> Optional[str]:
        "Returns the full path to the Icon"
        if self.Icon is None:
            return None
        else:
            return get_icon_path(self.Icon)

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, DesktopAction):
            return False

        return self.Name == obj.Name and self.Icon == obj.Icon and self.Exec == obj.Exec


class DesktopEntry:
    def __init__(self) -> None:
        self.Type: Literal["Application", "Link", "Directory"] = "Application"
        "The Type Key"

        self.Version: Optional[Literal["1.0", "1.1", "1.2", "1.3", "1.4", "1.5"]] = None
        "The Version Key"

        self.Name: TranslatableKey = TranslatableKey()
        "The Name Key"

        self.GenericName: TranslatableKey = TranslatableKey()
        "The GenericName Key"

        self.NoDisplay: Optional[bool] = None
        "The NoDisplay Key"

        self.Comment: TranslatableKey = TranslatableKey()
        "The Comment Key"

        self.Icon: Optional[str] = None
        "The Icon Key"

        self.Hidden: Optional[bool] = None
        "The Hidden Key"

        self.OnlyShowIn: list[str] = []
        "The OnlyShowIn Key"

        self.NotShowIn: list[str] = []
        "The NotShowIn Key"

        self.DBusActivatable: Optional[bool] = None
        "The DBusActivatable Key"

        self.TryExec: Optional[str] = None
        "The TryExec Key"

        self.Exec: Optional[str] = None
        "The Exec Key"

        self.Path: Optional[str] = None
        "The Path Key"

        self.Terminal: Optional[bool] = None
        "The Terminal Key"

        self.MimeType: list[str] = []
        "The MimeType Key"

        self.Categories: list[str] = []
        "The Categories Key"

        self.Implements: list[str] = []
        "The Implements Key"

        self.Keywords: TranslatableListKey = TranslatableListKey()
        "The Keywords Key"

        self.StartupNotify: Optional[bool] = None
        "The StartupNotify Key"

        self.URL: Optional[str] = None
        "The URL Key"

        self.PrefersNonDefaultGPU: Optional[bool] = None
        "The PrefersNonDefaultGPU Key"

        self.SingleMainWindow: Optional[bool] = None
        "The SingleMainWindow Key"

        self.Actions: dict[str, DesktopAction] = {}
        "The Actions"

        self.CustomKeys: dict[str, str] = {}
        "The Keys starting with X-"

        self.file_path: Optional[str] = None
        "The path to the .desktop file"

        self.desktop_id: Optional[str] = None
        "The ID of the .desktop file"

    def _execute_validate_command(self) -> subprocess.CompletedProcess:
        "Executes desktop-file-validate and returns the result"
        file_handle, temp_path = tempfile.mkstemp(suffix=".desktop")
        try:
            os.close(file_handle)
            self.write_file(temp_path)
            return subprocess.run(["desktop-file-validate", temp_path], capture_output=True)
        finally:
            os.remove(temp_path)

    def is_valid(self) -> bool:
        "Returns, if the desktop entry is valid. desktop-file-validate needs to be installed."
        return self._execute_validate_command().returncode == 0

    def get_validation_messages(self) -> ValidationMessageDict:
        "Returns all messages from desktop-file-validate"
        message_dict: ValidationMessageDict = {"Error": [], "FutureError": [], "Warning": [], "Hint": []}
        for i in self._execute_validate_command().stdout.decode("utf-8").splitlines():
            file_name, message_type, message = _strip_list(i.split(":", 2))
            if message_type == "error":
                if message.startswith("(will be fatal in the future): "):
                    message_dict["FutureError"].append(message.removeprefix("(will be fatal in the future): "))
                else:
                    message_dict["Error"].append(message)
            elif message_type == "warning":
                message_dict["Warning"].append(message)
            elif message_type == "hint":
                message_dict["Hint"].append(message)
        return message_dict

    def should_show(self) -> bool:
        "Returns if desktop entry should be showed"
        if self.Hidden:
            return False

        try:
            # According to the documentation, this is colon-separated list, in most cases it is just a single string
            desktop_list = os.environ("XDG_CURRENT_DESKTOP").split(";")
        except AttributeError:
            return True

        for i in self.NotShowIn:
            if i in desktop_list:
                return False

        if len(self.OnlyShowIn) != 0:
            for i in self.OnlyShowIn:
                if i in desktop_list:
                    return True
            return False
        else:
            return True

    def should_show_in_menu(self) -> bool:
        "Returns if a dektop entry should be displayed in the menu"
        return not self.NoDisplay and not self.should_hide()

    def get_icon_path(self) -> Optional[str]:
        "Returns the full path to the Icon"
        if self.Icon is None:
            return None
        else:
            return get_icon_path(self.Icon)

    def get_text(self) -> str:
        "Returns the content of the desktop entry"
        text = "[Desktop Entry]\n"
        text += f"Type={self.Type}\n"

        if self.Version is not None:
            text += f"Version={self.Version}\n"

        text += self.Name.get_text("Name")
        text += self.GenericName.get_text("GenericName")

        if self.NoDisplay is not None:
            text += f"NoDisplay={str(self.NoDisplay).lower()}\n"

        text += self.Comment.get_text("Comment")

        if self.Icon is not None:
            text += f"Icon={self.Icon}\n"

        if self.Hidden is not None:
            text += f"Hidden={str(self.Hidden).lower()}\n"

        if len(self.OnlyShowIn) != 0:
            text += "OnlyShowIn=" + ";".join(self.OnlyShowIn) + ";\n"

        if len(self.NotShowIn) != 0:
            text += "NotShowIn=" + ";".join(self.NotShowIn) + ";\n"

        if self.DBusActivatable is not None:
            text += f"Hidden={str(self.DBusActivatable).lower()}\n"

        if self.TryExec is not None:
            text += f"TryExec={self.TryExec}\n"

        if self.Exec is not None:
            text += f"Exec={self.Exec}\n"

        if self.Path is not None:
            text += f"Path={self.Path}\n"

        if self.Terminal is not None:
            text += f"Terminal={str(self.Terminal).lower()}\n"

        if len(self.MimeType) != 0:
            text += "MimeType=" + ";".join(self.MimeType) + ";\n"

        if len(self.Categories) != 0:
            text += "Categories=" + ";".join(self.Categories) + ";\n"

        if len(self.Implements) != 0:
            text += "Implements=" + ";".join(self.Implements) + ";\n"

        text += self.Keywords.get_text("Keywords")

        if self.StartupNotify is not None:
            text += f"StartupNotify={str(self.StartupNotify).lower()}\n"

        if self.URL is not None:
            text += f"URL={self.URL}\n"

        if self.PrefersNonDefaultGPU is not None:
            text += f"PrefersNonDefaultGPU={str(self.PrefersNonDefaultGPU).lower()}\n"

        if self.SingleMainWindow is not None:
            text += f"SingleMainWindow={str(self.SingleMainWindow).lower()}\n"

        if len(self.Actions) != 0:
            text += "Actions=" + ";".join(self.Actions.keys()) + ";\n"

        for key, value in self.CustomKeys.items():
            if key.startswith("X-"):
                text += f"{key}={value}\n"

        for key, value in self.Actions.items():
            text += f"\n[Desktop Action {key}]\n"
            text += value.get_text() + "\n"

        return text

    def write_file(self, path: Union[str, os.PathLike]) -> None:
        "Writes a .desktop file"
        try:
            os.makedirs(os.path.dirname(path))
        except (FileExistsError, FileNotFoundError):
            pass

        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(self.get_text())

    @classmethod
    def from_string(cls, text: str) -> "DesktopEntry":
        "Loads the content of a .desktop file from a string"
        entry = cls()

        sections = _parse_desktop_sections(text)

        if "Desktop Entry" not in sections:
            return entry

        entry.Type = sections["Desktop Entry"].get("Type", "Application")
        entry.Version = sections["Desktop Entry"].get("Version", None)
        entry.Name.load_section(sections["Desktop Entry"], "Name")
        entry.GenericName.load_section(sections["Desktop Entry"], "GenericName")
        entry.NoDisplay = _string_to_bool(sections["Desktop Entry"].get("NoDisplay", None))
        entry.Comment.load_section(sections["Desktop Entry"], "Comment")
        entry.Icon = sections["Desktop Entry"].get("Icon", None)
        entry.Hidden = _string_to_bool(sections["Desktop Entry"].get("Hidden", None))

        if "OnlyShowIn" in sections["Desktop Entry"]:
            entry.OnlyShowIn = sections["Desktop Entry"]["OnlyShowIn"].removesuffix(";").split(";")

        if "NotShowIn" in sections["Desktop Entry"]:
            entry.NotShowIn = sections["Desktop Entry"]["NotShowIn"].removesuffix(";").split(";")

        entry.DBusActivatable = _string_to_bool(sections["Desktop Entry"].get("DBusActivatable", None))
        entry.TryExec = sections["Desktop Entry"].get("TryExec", None)
        entry.Exec = sections["Desktop Entry"].get("Exec", None)
        entry.Path = sections["Desktop Entry"].get("Path", None)
        entry.Terminal = _string_to_bool(sections["Desktop Entry"].get("Terminal", None))

        if "MimeType" in sections["Desktop Entry"]:
            entry.MimeType = sections["Desktop Entry"]["MimeType"].removesuffix(";").split(";")

        if "Categories" in sections["Desktop Entry"]:
            entry.Categories = sections["Desktop Entry"]["Categories"].removesuffix(";").split(";")

        if "Implements" in sections["Desktop Entry"]:
            entry.Categories = sections["Desktop Entry"]["Implements"].removesuffix(";").split(";")

        entry.Keywords.load_section(sections["Desktop Entry"], "Keywords")
        entry.StartupNotify = _string_to_bool(sections["Desktop Entry"].get("StartupNotify", None))
        entry.URL = sections["Desktop Entry"].get("URL", None)
        entry.PrefersNonDefaultGPU = _string_to_bool(sections["Desktop Entry"].get("PrefersNonDefaultGPU", None))
        entry.SingleMainWindow = _string_to_bool(sections["Desktop Entry"].get("SingleMainWindow", None))

        if "Actions" in sections["Desktop Entry"]:
            for i in sections["Desktop Entry"]["Actions"].removesuffix(";").split(";"):
                entry.Actions[i] = DesktopAction.from_dict(sections[f"Desktop Action {i}"])

        for key, value in sections["Desktop Entry"].items():
            if key.startswith("X-"):
                entry.CustomKeys[key] = value

        return entry

    @classmethod
    def from_file(cls, path: Union[str, os.PathLike]) -> "DesktopEntry":
        "Returns a desktop entry from the given file"
        with open(path, "r", encoding="utf-8", newline="\n") as f:
            entry = cls.from_string(f.read())
            entry.file_path = os.path.abspath(path)
            entry.desktop_id = os.path.basename(path).removesuffix(".desktop")
            return entry

    @classmethod
    def from_id(cls, desktop_id: str) -> Optional["DesktopEntry"]:
        "Returns a desktop entry from the given id"
        for i in get_xdg_data_dirs():
            entry_path = os.path.join(i, "applications", desktop_id + ".desktop")
            if os.path.isfile(entry_path):
                return cls.from_file(entry_path)

    def __repr__(self) -> str:
        return f"<DesktopEntry Name='{self.Name.default_text}'>"

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, DesktopEntry):
            return False

        try:
            assert self.Type == obj.Type
            assert self.Version == obj.Version
            assert self.Name == obj.Name
            assert self.GenericName == obj.GenericName
            assert self.NoDisplay == obj.NoDisplay
            assert self.Comment == obj.Comment
            assert self.Icon == obj.Icon
            assert self.Hidden == obj.Hidden
            assert self.OnlyShowIn == obj.OnlyShowIn
            assert self.NotShowIn == obj.NotShowIn
            assert self.DBusActivatable == obj.DBusActivatable
            assert self.TryExec == obj.TryExec
            assert self.Exec == obj.Exec
            assert self.Path == obj.Path
            assert self.Terminal == obj.Terminal
            assert self.MimeType == obj.MimeType
            assert self.Categories == obj.Categories
            assert self.Implements == obj.Implements
            assert self.Keywords == obj.Keywords
            assert self.StartupNotify == obj.StartupNotify
            assert self.URL == obj.URL
            assert self.PrefersNonDefaultGPU == obj.PrefersNonDefaultGPU
            assert self.SingleMainWindow == obj.SingleMainWindow
            assert _compare_dict(self.Actions, obj.Actions)
            assert _compare_dict(self.CustomKeys, obj.CustomKeys)
            return True
        except AssertionError:
            return False


class DesktopEntryCollection:
    def __init__(self) -> None:
        self.desktop_entries: dict[str, DesktopEntry] = {}
        "The desktop entries"

    def load_file(self, path: Union[str, os.PathLike]):
        "Loads the given file"
        entry = DesktopEntry.from_file(path)
        self.desktop_entries[os.path.basename(path).removesuffix(".desktop")] = entry

    def load_directory(self, path: Union[str, os.PathLike]) -> None:
        "Loads all desktop entries from the given directory"
        for i in os.listdir(path):
            if i.endswith(".desktop"):
                self.load_file(os.path.join(path, i))

    def load_menu(self) -> None:
        "Loads all desktop entries from the menu"
        for i in get_xdg_data_dirs():
            menu_dir = os.path.join(i, "applications")
            if os.path.isdir(menu_dir):
                self.load_directory(menu_dir)

    def load_desktop(self) -> None:
        "Loads all desktop entries files from the Desktop"
        desktop_path = subprocess.check_output(["xdg-user-dir", "DESKTOP"]).decode("utf-8").strip()
        if os.path.isdir(desktop_path):
            self.load_directory(desktop_path)

    def load_autostart(self) -> None:
        "Loads all autostart entries"
        for i in ("/run/host/etc/xdg/autostart" if _is_flatpak() else "/etc/xdg/autostart", os.path.expanduser("~/.config/autostart/")):
            if os.path.isdir(i):
                self.load_directory(i)

    def get_entries_by_category(self, category: str) -> list[DesktopEntry]:
        "Returns a list of all desktop entries that have the given category"
        entry_list = []
        for i in self.desktop_entries.values():
            if category in i.Categories:
                entry_list.append(i)
        return entry_list

    def get_entries_by_mime_type(self, mime_type: str) -> list[DesktopEntry]:
        "Returns a list of all desktop entries that can open the given MimeType"
        entry_list = []
        for i in self.desktop_entries.values():
            if mime_type in i.MimeType:
                entry_list.append(i)
        return entry_list

    def get_visible_entries(self) -> list[DesktopEntry]:
        "Get a list of all desktop enties that should be shown to the User"
        entry_list = []
        for i in self.desktop_entries.values():
            if i.should_show():
                entry_list.append(i)
        return entry_list

    def get_menu_entries(self) -> list[DesktopEntry]:
        "Get a list of all desktop enties that should be shown in the Menu"
        entry_list = []
        for i in self.desktop_entries.values():
            if i.should_show_in_menu():
                entry_list.append(i)
        return entry_list

    def __len__(self) -> int:
        return len(self.desktop_entries)

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, DesktopEntryCollection):
            return False

        return _compare_dict(self.desktop_entries, obj.desktop_entries)

    def __getitem__(self, name: str) -> DesktopEntry:
        return self.desktop_entries[name]

    def __setitem__(self, key: str, value: DesktopEntry) -> None:
        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        if not isinstance(value, DesktopEntry):
            raise ValueError("Value must be a DesktopEntry")

        self.desktop_entries[key] = value

    def __contains__(self, name: str) -> bool:
        return name in self.desktop_entries 
