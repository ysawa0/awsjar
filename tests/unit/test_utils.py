import pytest

from awsjar.utils import datetime_encoder, _data_dumper, _convert_str_to_number


def test_datetime_encoder():
    with pytest.raises(TypeError):
        datetime_encoder({"invalid obj for encoder"})


def test_convert_str_to_number():
    assert _convert_str_to_number("123") == 123
    assert _convert_str_to_number("0") == 0
    assert _convert_str_to_number("-12") == 0

    assert _convert_str_to_number("12.3") == 12.3
    assert _convert_str_to_number("0.0") == 0.0
    assert _convert_str_to_number("-1.2") == -1.2

    assert _convert_str_to_number("123asd") == "123asd"
    assert _convert_str_to_number("12a312") == "12a312"
    assert _convert_str_to_number("asdfasdf") == "asdfasdf"
