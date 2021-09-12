from ..builders import Configuration
from .transform import group_lookup
from .consume import open_file, consume_config


def parse(fname: str, **kwargs) -> Configuration:
    config = open_file(fname, **kwargs)
    return consume_config(config)
