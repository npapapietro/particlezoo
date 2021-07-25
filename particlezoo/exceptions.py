class ConfigError(Exception):
    pass

class ModelError(Exception):
    """Raised when something nonphysical is passed in like spin 1/10"""
    pass