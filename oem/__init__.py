from oem.core.exceptions import AbsoluteNumberRequiredError

try:
    from oem.client import Client
    OemClient = Client
except ImportError:
    Client = None
    OemClient = None
