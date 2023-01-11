# This file is part of emzed (https://emzed.ethz.ch), a software toolbox for analysing
# LCMS data with Python.
#
# Copyright (C) 2020 ETH Zurich, SIS ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


import os
import shutil
import subprocess
import sys
import time
import venv
import weakref
from multiprocessing.connection import Client
from threading import Thread

import numpy as np

PYOPENMS_VERSION = "2.7.0"


def encode(s):
    if isinstance(s, str):
        return s.encode("utf-8")
    return s


def decode(s):
    if isinstance(s, bytes):
        return str(s, "utf-8")
    return s


_map = {}


def register(id_):
    obj = ObjectProxy(id_)
    _map[id_] = obj
    return obj


BASIC_TYPES = (int, float, str, bool, bytes, type(None))

OBJECT_PROXY = 1
ND_ARRAY = 2


def unwrap(data):
    type_, item = data

    if type_ is OBJECT_PROXY:
        id_ = item
        if id_ in _map:
            return _map[id_]
        return register(id_)

    if type_ is ND_ARRAY:
        bytes_, shape, dtype = item
        return np.ndarray(shape, dtype, bytes_)

    if isinstance(item, BASIC_TYPES):
        return item

    if isinstance(item, list):
        return [unwrap(ii) for ii in item]
    if isinstance(item, tuple):
        return tuple(unwrap(ii) for ii in item)
    if isinstance(item, set):
        return set(unwrap(ii) for ii in item)
    if isinstance(item, dict):
        return {unwrap(key): unwrap(value) for key, value in item.items()}

    raise NotImplementedError(f"don't know how to unwrap {item!r}")


def wrap(data):
    if isinstance(data, BASIC_TYPES):
        if getattr(data, "__module__", "").startswith("emzed."):
            raise ValueError("you must not pass emzed object to pyopenms")
        return 0, data

    if isinstance(data, list):
        return 0, [wrap(ii) for ii in data]
    if isinstance(data, tuple):
        return 0, tuple(wrap(ii) for ii in data)
    if isinstance(data, set):
        return 0, set(wrap(ii) for ii in data)
    if isinstance(data, dict):
        return 0, {wrap(key): wrap(value) for key, value in data.items()}

    if isinstance(data, ObjectProxy):
        return OBJECT_PROXY, data.id_

    if isinstance(data, np.ndarray):
        return ND_ARRAY, (data.tobytes(), data.shape, data.dtype.name)

    raise NotImplementedError(f"dont know how to wrap {data!r}")


here = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(here, "_pyopenms_venv")


if sys.platform == "win32":
    pip_exe = f"{os.path.join(env_path, 'Scripts', 'pip.exe')}"
    pip = f"{os.path.join(env_path, 'Scripts', 'python.exe -m pip')}"
    python_venv_exe = f"{os.path.join(env_path, 'Scripts', 'python.exe')}"
else:
    pip_exe = f"{os.path.join(env_path, 'bin', 'pip')}"
    pip = pip_exe
    python_venv_exe = f"{os.path.join(env_path, 'bin', 'python')}"

if os.path.exists(pip_exe):
    failed = False
    try:
        pyopenms_info = subprocess.check_output(
            f"{pip} show pyopenms",
            text=True,
            shell=True,
        ).split("\n")
    except subprocess.CalledProcessError:
        failed = True
    else:
        version_line = [
            line.strip() for line in pyopenms_info if "version:" in line.lower()
        ]
        assert len(version_line) == 1, "pip show pyopenms failed!"
        version = version_line[0].split(":")[1].strip()
        if version != PYOPENMS_VERSION:
            failed = True

    if failed:
        print("upgrade pyopenms")
        shutil.rmtree(env_path)


# don't use else here!
if not os.path.exists(pip_exe):
    venv.create(env_path, with_pip=True)

    try:
        assert os.system(f"{pip} install -U pip") == 0
        assert (
            os.system(
                f"{pip} install -U pyopenms=={PYOPENMS_VERSION}"
                f" numpy=={np.__version__}"
            )
            == 0
        )
    except Exception:
        try:
            pass
            # shutil.rmtree(env_path)
        except Exception:
            pass
        raise


def start_remote_pyopenms():
    port = None
    proc = None

    def start_listener():
        nonlocal port, proc
        with subprocess.Popen(
            [
                python_venv_exe,
                "-u",
                f"{os.path.join(here, 'pyopenms_client.py')}",
                env_path,
            ],
            stdout=subprocess.PIPE,
            text=True,
        ) as proc:
            for l in iter(proc.stdout.readline, ""):
                l = l.rstrip()
                if l.startswith("PORT="):
                    _, _, port = l.partition("=")
                    print("pyopenms client started.")
                    continue
                print(f"pyopenms: {l}", flush=True)

    t = Thread(target=start_listener)
    t.daemon = True
    t.start()

    while True:
        if port is None:
            time.sleep(0.1)
            continue
        try:
            conn = Client(("127.0.0.1", int(port)), authkey=b"secret password")
            break
        except ConnectionRefusedError:
            time.sleep(0.1)
            continue
    print("connected to pyopenms client.")
    return conn, proc


class DirWrapper:
    def __init__(self, dir_):
        self.dir_ = dir_

    def __iter__(self):
        return iter(self.dir_)


class ObjectProxy:
    _map = dict()
    conn = None

    def __init__(self, id_):
        self.id_ = id_
        ObjectProxy._map[id_] = self
        weakref.finalize(self, self._del_obj_callback, id_)

    @staticmethod
    def _del_obj_callback(id_):
        try:
            ObjectProxy._send("DELETE", id_)
        except IOError:
            # endpoint is already dead
            pass

    @staticmethod
    def _send(command, *args):
        args = wrap(args)
        ObjectProxy.conn.send((command, args))

    @staticmethod
    def _recv():
        while not ObjectProxy.conn.poll(timeout=0.001):
            pass
        error, result = ObjectProxy.conn.recv()
        if error:
            raise error
        return unwrap(result)

    def __dir__(self):
        self._send("DIR", self)
        return DirWrapper(self._recv())

    def __getstate__(self):
        raise NotImplementedError()

    def __setstate__(self, _):
        raise NotImplementedError()

    def __call__(self, *a, **kw):
        self._send("CALL", self, a, kw)
        result, a_after = self._recv()
        for a_i, a_after_i in zip(a, a_after):
            if isinstance(a_i, list):
                a_i[:] = a_after_i
        return result

    def __setitem__(self, key, value):
        self._send("SETITEM", self, key, value)
        return self._recv()

    def __getitem__(self, key):
        self._send("GETITEM", self, key)
        return self._recv()

    def __getattr__(self, name):
        self._send("GETATTR", self, name)
        return self._recv()

    def __iter__(self):
        self._send("ITER", self)
        iter_obj = self._recv()
        while True:
            self._send("NEXT", iter_obj)
            try:
                yield self._recv()
            except StopIteration:
                break


class PyOpenMS(ObjectProxy):
    def __init__(self):
        self.id_ = -1
        _map[-1] = self
        conn, proc = start_remote_pyopenms()
        ObjectProxy.conn = conn
        weakref.finalize(self, PyOpenMS.deleted_callback, conn, proc)

    def __spec__(self):
        return None

    @staticmethod
    def deleted_callback(conn, proc):
        try:
            PyOpenMS._send("KILLPILL")
        except IOError:
            # endpoint is already dead
            pass
        try:
            proc.terminate()
        except IOError:
            # endpoint is already dead
            pass


pyopenms = sys.modules["pyopenms"] = PyOpenMS()
