import os
import stat
import json
import yaml
import pytest
from hash import core, resources, store, errors
from hash import utils
from hash.utils import Artifact, Artifacts, Globals, ImDict
from .commons import create_resource_file, create_local_file_store_config
#def test_globals_class(tmp_path):
#    config = create_local_file_store_config(tmp_path)
#    s = store.get_store("LocalFile", config)
#    resources.setup(tmp_path, s)
#    state = {
#        "hash": "hash",
#        "state": "build",
#        "build": {
#            "globals": {
#                "x": "a"
#            }
#        }
#    }
#    res_dir = tmp_path / "res_dir"
#    res_dir.mkdir()
#    create_resource_file(res_dir / "resource.yaml", "Fake", "hashio", {"path": str(res_dir)})
#    r = resources.Resource(res_dir / "resource.yaml")
#    s.store(state, r)
#    globals = Globals(s.get_globals(), {}, True)
#    globals.get("Fake:hashio", "build", "x")
#    assert globals.deps == [("Fake:hashio", "build")]

def test_imdict1():
    d = {}
    im1 = utils.ImDict(d)
    with pytest.raises(KeyError):
        im1["x"]

def test_imdict2():
    d = {
        "x": 1
    }
    im1 = utils.ImDict(d)
    assert im1["x"] == 1
    d["x"] = 2
    assert im1["x"] == 2

def test_imdict3():
    d = {
        "x": {
            "r": 1
        }
    }
    im1 = utils.ImDict(d)
    assert im1["x"]["r"] == 1
    dd = im1["x"]
    assert dd["r"] == 1
    with pytest.raises(errors.DictError):
        dd["r"] = 2
    assert im1["x"]["r"] == 1

def test_imdict_list():
    d = {
        "x": {
            "r": 1
        },
        "y": ["1"]
    }
    im1 = utils.ImDict(d)
    l = im1["y"]
    assert len(l) == 1
    assert type(l) == tuple

def test_imdict1_get():
    d = {
        "x": 9,
        "r": ["e", 1],
        "d": True,
        "f": {
            "a": 90
        }
    }
    im1 = utils.ImDict(d)
    assert im1.get("x") == 9

def test_imdict1_keys():
    d = {
        "x": 9,
        "r": ["e", 1],
        "d": True,
        "f": {
            "a": 90
        }
    }
    im1 = utils.ImDict(d)
    keys = im1.keys()
    assert len(keys) == 4
    assert "x" in keys
    assert "r" in keys
    assert "d" in keys
    assert "f" in keys

def test_imdict_data():
    d = {
        "x": 9
    }
    im1 = utils.ImDict(d)
    _d = im1._data()
    _d["x"] = 1
    assert im1.get("x") == 9

def test_imdict_nested_dict():
    d = {
        "x": {
            "a": 123
        }
    }
    im1 = utils.ImDict(d)
    assert im1["x"]["a"] == 123
    assert type(im1["x"]) == utils.ImDict
    assert im1.get("x")["a"] == 123
    assert type(im1.get("x")) == utils.ImDict

def test_imdict_nested_list():
    d = {
        "x": {
            "a": 123
        },
        "l": ["123", "4fa"]
    }
    im1 = utils.ImDict(d)
    assert im1["l"][0] == "123"
    assert type(im1["l"]) == tuple
    assert im1.get("l")[0] == "123"
    assert type(im1.get("l")) == tuple

def test_imdict_eq():
    d1 = {
        "x": 123
    }
    d2 = d1
    im1 = utils.ImDict(d1)
    im2 = utils.ImDict(d2)
    assert im1 == im2
    im3 = utils.ImDict({"a": 90})
    assert im1 != im3

def test_imdict_json():
    d = {
        "x": 1
    }
    im1 = utils.ImDict(d)
    dd = json.loads(json.dumps(im1, cls=utils.HashJsonEncoder))
    assert dd["x"] == 1

def test_imdict_no_dict():
    with pytest.raises(errors.DictError):
        utils.ImDict("a")

def test_parse_no_file():
    with pytest.raises(FileNotFoundError):
        utils.parse_resource_file("a")

def test_parse_number():
    with pytest.raises(FileNotFoundError):
        utils.parse_resource_file(9)

def test_parse_invalid_yaml(tmp_path):
    f = tmp_path / "resource.yaml"
    f.write_text("""
    sd:ua
    yu:
        - 9a
    """)
    with pytest.raises(errors.ResourceInvalidYaml):
        utils.parse_resource_file(str(f))

def test_parse_no_yaml(tmp_path):
    f = tmp_path / "resource.yaml"
    f.write_text("a")
    with pytest.raises(errors.ResourceError):
        utils.parse_resource_file(str(f))


def test_parse_no_kind(tmp_path):
    d = {}
    f = tmp_path / "resource.yaml"
    f.write_text(yaml.dump(d))
    with pytest.raises(errors.ResourceError):
        utils.parse_resource_file(str(f))

def test_parse_no_metadata(tmp_path):
    d = {
        "kind": "a"
    }
    f = tmp_path / "resource.yaml"
    f.write_text(yaml.dump(d))
    with pytest.raises(errors.ResourceError):
        utils.parse_resource_file(str(f))

def test_parse_str_metadata(tmp_path):
    d = {
        "kind": "a",
        "metadata": "a"
    }
    f = tmp_path / "resource.yaml"
    f.write_text(yaml.dump(d))
    with pytest.raises(errors.ResourceError):
        utils.parse_resource_file(str(f))

def test_parse_no_name(tmp_path):
    d = {
        "kind": "a",
        "metadata": {
            "x": 1
        }
    }
    f = tmp_path / "resource.yaml"
    f.write_text(yaml.dump(d))
    with pytest.raises(errors.ResourceError):
        utils.parse_resource_file(str(f))

def test_parse_no_error(tmp_path):
    d = {
        "kind": "a",
        "metadata": {
            "name": "asd"
        }
    }
    f = tmp_path / "resource.yaml"
    f.write_text(yaml.dump(d))
    d = utils.parse_resource_file(str(f))
    assert d["kind"] == "a"
    assert d["metadata"]["name"] == "asd"

def test_artifact1():
    aft = utils.Artifact("id", "build", "dev", "asd", "url", "https://hash.io")
    assert aft.getId() == "id"
    assert aft.getAction() == "build"
    assert aft.getEnv() == "dev"
    assert aft.getHash() == "asd"
    assert aft.getKind() == "url"
    assert aft.getData() == "https://hash.io"

def test_artifact_equal():
    aft1 = utils.Artifact("id", "build", "dev", "asd", "url", "https://hash.io")
    aft2 = utils.Artifact("id", "build", "dev", "asd", "url", "https://hash.io")
    assert aft1 == aft2

def test_artifact_not_equal():
    aft1 = utils.Artifact("id", "build", "dev", "asd1", "url", "https://hash.io")
    aft2 = utils.Artifact("id", "build", "dev", "asd", "url", "https://hash.io")
    assert aft1 != aft2

def test_read_artifact_no_id():
    aft = {}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_no_action():
    aft = {"id": "a"}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_wrong_action():
    aft = {"id": "a", "action": "a"}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_no_kind():
    aft = {"id": "a", "action": "build"}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_wrong_kind():
    aft = {"id": "a", "action": "build", "kind": "a"}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_wrong_env():
    aft = {"id": "a", "action": "build", "kind": "text", "env": 1}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_no_hash():
    aft = {"id": "a", "action": "build", "kind": "text"}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_no_data():
    aft = {"id": "a", "action": "build", "kind": "text", "hash": "a"}
    with pytest.raises(errors.ArtifactError):
        Artifact.read_artifact(aft)

def test_read_artifact_no_error():
    aft = {
        "id": "a",
        "hash": "h",
        "kind": "text",
        "data": "a",
        "action": "build"
    }
    af = Artifact.read_artifact(aft)
    assert af.getAction() == "build"
    assert af.getId() == "a"
    assert af.getData() == "a"
    assert af.getEnv() is None
    assert af.getHash() == "h"

def test_artifact2(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("artifact test")
    aft = utils.Artifact("id", "build", "dev", "asd", "file", str(f))
    assert aft.getData() == str(f)

def test_artifact3():
    with pytest.raises(FileNotFoundError):
        utils.Artifact("id", "build", "dev", "asd", "file", "a")

def test_artifact4(tmp_path):
    file_data = b"hello artifact"
    with pytest.raises(FileNotFoundError):
        open(tmp_path / "test.txt", "r")
    utils.Artifact("id", "build", "dev", "asd", "file", str(tmp_path / "test.txt"), file_data=file_data)
    with open(tmp_path / "test.txt", "rb") as f:
        assert f.read() == file_data
    aft = utils.Artifact("id", "build", "dev", "asd", "file", str(tmp_path / "test.txt"))
    assert aft.getData() == str(tmp_path / "test.txt")

def test_artifact5(tmp_path):
    file_data = b"hello artifact"
    with pytest.raises(FileNotFoundError):
        open(tmp_path / "test.txt", "r")
    aft = utils.Artifact("id", "build", "dev", "asd", "file", str(tmp_path / "test.txt"), file_data=file_data)
    assert aft.file_name() == "artifact-id-build-dev-asd"

def test_artifact6(tmp_path):
    file_data = b"hello artifact"
    with pytest.raises(FileNotFoundError):
        open(tmp_path / "test.txt", "r")
    aft = utils.Artifact("id", "build", "dev", "asd", "file", str(tmp_path / "test.txt"), file_data=file_data)
    assert aft.getDict()["id"] == "id"
def test_artifact7():
    with pytest.raises(errors.ArtifactError):
        utils.Artifact("d", "build", "dev", "asd", "a", "a")

def test_script1():
    with pytest.raises(errors.ScriptError):
        utils.Script(1)

def test_script2():
    with pytest.raises(errors.ScriptError):
        utils.Script("a")

def test_script3(tmp_path):
    script_file = tmp_path / "test.sh"
    script_file.write_text("""#!/bin/bash
echo -n 123 > t.txt
    """)
    st = os.stat(str(script_file))
    os.chmod(script_file, st.st_mode | stat.S_IEXEC)
    sc = utils.Script(str(script_file))
    sc.run(tmp_path)
    with open(tmp_path / "t.txt") as f:
        assert f.read() == "123"

def test_script4(tmp_path):
    sc = utils.Script()
    sc.execute("echo -n 123 > t.txt", tmp_path)
    with open(tmp_path / "t.txt") as f:
        assert f.read() == "123"
