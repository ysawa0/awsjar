import logging

from awsjar.jar import Jar  # noqa: F401
from awsjar.bucket import Bucket  # noqa: F401

from awsjar.utils import datetime_encoder, datetime_decoder  # noqa: F401

from awsjar._version import get_versions

__version__ = get_versions()["version"]
del get_versions


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# Configure default logger to do nothing
log = logging.getLogger("awsjar")
log.addHandler(NullHandler())
