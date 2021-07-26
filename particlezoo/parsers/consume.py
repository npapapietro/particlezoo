import json
import yaml
import toml
from typing import cast, Union
from os.path import splitext

from ..exceptions import ConfigError
from ..datamodels import Configuration, SymmetryGroup, GenericField


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


def open_file(fname: str, opener=None, **kwargs) -> dict:
    """Opens file into a raw dictionary."""
    if opener is None:
        opener = decide_opener(fname)
    return opener(fname)


def consume_representation(config: Union[str, list]) -> Union[str, list]:
    """Consumes the representation on the GenericField"""

    if isinstance(config, (list, str)):
        return config
    elif isinstance(config, int):  # SU_2, integer charges, etc
        return str(config)
    raise ConfigError("Representation must be a string or list")


def consume_symmetry(config: dict) -> SymmetryGroup:
    """Consumes the symmetry on the config"""
    description = config.get("description", "")

    group = config.get("group", "")
    if group.strip() == "":
        raise ConfigError("`group` required on `symmetries`.")

    name = config.get("name", "")
    if name.strip() == "":
        raise ConfigError("`name` required on `fields`.")

    return SymmetryGroup(description=description, name=name, group=group)


def consume_fields(config: dict) -> GenericField:
    """Consumes the field on the config"""
    name = config.get("name", "")
    if name.strip() == "":
        raise ConfigError("`name` required on `fields`.")

    spin = config.get("spin", "")
    if spin.strip() == "":
        raise ConfigError("`spin` required on `fields`.")

    description = config.get("description", "")

    representations = config.get("representations", {})
    if not isinstance(representations, dict):
        raise ConfigError(
            "`representations` on `fields` must be a dictionary")
    representations = {k: consume_representation(v)
                       for k, v in representations.items()}

    return GenericField(name=name, spin=spin, description=description, representations=representations)


def consume_config(config: dict) -> Configuration:
    """Consumes at the top level the file as dictionary.

    Args:
        config (dict): Raw dictionary from file.

    Raises:
        ConfigError: If required field is not present

    Returns:
        Configuration: Instance of configuration.
    """

    name: str = config.get("name", "")
    if name.strip() == "":
        raise ConfigError("`name` required on configuration.")

    version = config.get("version")
    description = config.get("description")

    symmetries = config.get("symmetries", [])
    symmetries = [consume_symmetry(x) for x in symmetries]

    fields = config.get("fields", [])
    fields = [consume_fields(x) for x in fields]

    return Configuration(
        name=name,
        version=version,
        description=description,
        symmetries=symmetries,
        fields=fields
    )
