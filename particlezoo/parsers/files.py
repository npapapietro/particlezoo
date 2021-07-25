import json
import yaml
import toml
from typing import cast
from os.path import splitext

from ..exceptions import ConfigError


def open_toml(fname: str) -> dict:
    """Toml opening function"""
    with open(fname) as f:
        return cast(dict, toml.load(f))


def open_yaml(fname: str) -> dict:
    """Yaml opening function"""
    with open(fname) as f:
        return cast(dict, yaml.load(f))


def open_json(fname: str) -> dict:
    """Json opening function"""
    with open(fname) as f:
        return cast(dict, json.load(f))

def decide_opener(fname: str):
    """Chooses which function to open"""
    _, ext = splitext(fname)

    if ext == "yaml" or ext == "yml":
        return open_yaml
    if ext == "json":
        return open_json
    if ext == "toml":
        return open_toml

    return ConfigError("Unsupported config file")

def open_file(fname: str, opener=None) -> dict:
    """Opens file"""
    if opener is None:
        opener = decide_opener(fname)
    return opener(fname)

