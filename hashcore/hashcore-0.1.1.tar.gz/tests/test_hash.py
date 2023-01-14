"""
Main hash testing module
"""

import pytest
import os
import json

from hash import hash, store, resources

from .commons import create_resource_file


@pytest.mark.parametrize("data,expected", [
    ("mouhsen", "f8f1bd79c7c08d3b783debc263ad1563a1e4e56961a09beb4ab18030cc1a98ed"),
    ("sami", "f4babf63e1b75c361fd1726fff5a488e5367bb5dd0feaaa9d7207910bc9e3d56"),
    ("areen", "f4d4b7ab14850fd955af53f4fa08e05c810b742c13bc56ae69ee665f9f873e63")
    ])
def test_simple_sha256(data, expected, tmp_path):
    c_hash = hash.Hash()
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(data)
    h = c_hash.hash(d)
    assert h == expected

@pytest.mark.parametrize("data,expected", [
    ("mouhsen", "3ebab385a921d5a6a9d575b0e2343270"),
    ("sami", "77dc8a78aec78fc0d8bd2d45c4d8ddaf"),
    ("areen", "a63c265d18f2431af89e63231533527f")
    ])
def test_simple_md5(data, expected, tmp_path):
    c_hash = hash.Hash(alg="md5")
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(data)
    h = c_hash.hash(d)
    assert h == expected

def test_no_path(tmp_path):
    c_hash = hash.Hash(alg="md5")
    d = tmp_path / "sub"
    d.mkdir()
    pytest.raises(ValueError, c_hash.hash, str(d) + "no")

def test_unsupported_algorithm():
    pytest.raises(ValueError, hash.Hash, alg="hi")

def test_hash_represenattion():
    h = hash.Hash()
    assert repr(h) == '<Hash alg: sha256>'
    h = hash.Hash("md5")
    assert repr(h) == '<Hash alg: md5>'

@pytest.mark.parametrize("data,expected", [
    ("mouhsen", "f8f1bd79c7c08d3b783debc263ad1563a1e4e56961a09beb4ab18030cc1a98ed"),
    ("sami", "f4babf63e1b75c361fd1726fff5a488e5367bb5dd0feaaa9d7207910bc9e3d56"),
    ("areen", "f4d4b7ab14850fd955af53f4fa08e05c810b742c13bc56ae69ee665f9f873e63")
    ])
def test_simple_sha256_match(data, expected, tmp_path):
    c_hash = hash.Hash()
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(data)
    p = d / "hello"
    p.write_text(data)
    h = c_hash.hash(d, match=["*.txt"])
    assert h == expected
