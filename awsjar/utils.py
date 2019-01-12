import datetime

from awsjar.exceptions import ClientError


def _data_dumper(data, dumps):
    if isinstance(data, list) or isinstance(data, dict):
        data = dumps(data)
    else:
        raise ClientError(f"data to put is not a dict or list: {type(data)}")
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
