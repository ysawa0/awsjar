import zlib
import base64
import datetime


def _data_dumper(data, dumps):
    if isinstance(data, list) or isinstance(data, dict):
        data = dumps(data)
    else:
        data = str(data)
    return data


def datetime_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return {"_dt_": True, "repr": repr(obj)}
    else:
        type_name = obj.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")


def datetime_decoder(dct):
    if "_dt_" in dct:
        return eval(dct["repr"])
    return dct


def _compress(data, compression_level=9):
    assert (
        -1 <= compression_level <= 9
    ), "Compression level must be between -1 to 9, inclusive"
    data = data.encode()
    data = zlib.compress(data, level=compression_level)
    data = base64.b64encode(data)
    return data.decode()


def _decompress(data):
    if not data:
        return "{}"
    data = data.encode()
    data = base64.b64decode(data)
    data = zlib.decompress(data)
    return data.decode()


def _convert_str_to_number(st):
    try:
        st = float(st)
        return st
    except ValueError:
        pass
    try:
        st = int(st)
        return st
    except ValueError:
        pass
    return st
