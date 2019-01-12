import pytest

from awsjar.utils import datetime_encoder, _data_dumper
from awsjar.exceptions import ClientError


def test_datetime_encoder():
    with pytest.raises(TypeError):
        datetime_encoder({"invalid obj for encoder"})


def test_data_dumper():
    with pytest.raises(ClientError):
        _data_dumper({"invalid obj"}, None)
