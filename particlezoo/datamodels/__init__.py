"""Responsible for consuming and parsing the configuration files and 
converting them into data classes, namedtuples and model classes.

Structs are comprised of basic types incoming from the configuration file (yaml, json, toml)
and then parsed into instances.
"""

from .models import GenericField
from .structs import Representation