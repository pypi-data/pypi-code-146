# FlexiRPG -- Configurable settings database.
#
# Copyright 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import copy
import re
import sqlite3

import wx


class Setting:
    def __init__(self, collection: "SettingCollection", name: str, default):
        self._collection = collection
        self._name = name
        self._default = default
        self._value = copy.copy(default)
        self._watches = []

    @property
    def name(self):
        return self._name

    @property
    def default(self):
        return self._default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if type(val) != type(self._default):
            raise TypeError(f"Wrong type of {self._name} setting")
        if val == self._value:
            return

        self._value = copy.copy(val)
        self._collection._save(self)
        for watch in self._watches:
            watch(self)

    def watch(self, on_changed):
        """Add a callback function to be called when a setting changes."""
        self._watches.append(on_changed)

    def encode(self):
        type_ = type(self._default)
        if type_ == str:
            return self._value
        elif type_ == int:
            return str(self._value)
        elif type_ == bool:
            return "true" if self._value else "false"
        elif type_ == wx.Colour:
            c = self._value
            return f"rgba({c.Red()},{c.Green()},{c.Blue()},{c.Alpha()})"

    _rgba_regex = re.compile(r"rgba\((\d+),(\d+),(\d+),(\d+)\)")

    def decode(self, string):
        type_ = type(self._default)
        if type_ == str:
            self._value = string
        elif type_ == int:
            try:
                self._value = int(string)
            except ValueError:
                pass
        elif type_ == bool:
            self._value = string == "true"
        elif type_ == wx.Colour:
            m = self._rgba_regex.match(string)
            if m:
                self.value.Set(int(m.group(1)), int(m.group(2)),
                               int(m.group(3)), int(m.group(4)))


class SettingCollection:
    """A collection of configuration settings.

    Settings are saved to an SQLite database file.

    """

    def __init__(self, config_path):
        self._all = {} # All settings, indexed by name.
        self._connection = self._connect_to_db(config_path)

    def define(self, name: str, default) -> Setting:
        """Define a new setting.

        If the setting exists in the database, its value is applied.

        """

        if name in self._all:
            raise KeyError(f"Duplicate setting {name}")
        if type(default) not in (str, int, bool, wx.Colour):
            raise TypeError(f"Setting {name} has unsupported type {type(default)}")

        setting = Setting(self, name, default)
        self._all[name] = setting

        # Read the setting value form the DB (if it exists).
        c = self._connection.cursor()
        c.execute("SELECT value FROM settings WHERE name=?", (name,))
        result = c.fetchone()
        if result is not None:
            setting.decode(result[0])
        return setting

    def lookup(self, name: str) -> Setting:
        return self._all[name]

    def _connect_to_db(self, config_path):
        conn = sqlite3.connect(config_path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS settings (name text UNIQUE, value text)")
        conn.commit()
        return conn

    def _save(self, setting):
        c = self._connection.cursor()
        name = setting.name
        value = setting.encode()
        c.execute("INSERT OR IGNORE INTO settings (name, value) VALUES (?, ?)",
                  (name, value))
        c.execute("UPDATE settings SET value=? WHERE name=?",
                  (value, name))
        self._connection.commit()
