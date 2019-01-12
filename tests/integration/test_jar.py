from datetime import datetime as dt

import pytest
import botocore
from pprintpp import pprint

from awsjar import Jar, datetime_decoder, datetime_encoder
from awsjar.exceptions import ClientError

lambda_name = "jar-integration-test"
region = "us-east-1"


@pytest.fixture
def jar():
    return Jar(lambda_name=lambda_name, region=region)


def test_put_invalid_data_to_lambda(jar):
    data = "invalid data"
    with pytest.raises(ClientError):
        jar.put(data)


def test_put_dict_to_lambda(jar):
    data = {"list": [1, 23, 4, 5], "xyz": "xyz", "dt1": dt.now()}

    resp = jar.put(data)
    pprint(resp)

    assert resp == 200


def test_put_list_to_lambda(jar):
    data = [
        1,
        2,
        3,
        4,
        5,
        {"test": "example"},
        ["a", "b", {"test": "test"}],
        {"dt1": dt.now()},
    ]
    resp = jar.put(data)
    pprint(resp)

    assert resp == 200


def test_put_list_to_lambda_then_get(jar):
    time = dt.now()
    data = [
        1,
        2,
        3,
        4,
        5,
        {"test": "example"},
        ["a", "b", {"test": "test"}],
        {"dt1": time},
    ]
    pprint(data)

    resp = jar.put(data)
    pprint(resp)

    assert resp == 200
    jar_res = jar.get()
    jar_res[7] = str(time)
    data[7] = str(time)
    assert jar_res == data


def test_put_dict_to_lambda_then_get(jar):
    time = dt.now()

    data = {"list": [1, 23, 4, 5], "xyz": "xyz", "dt1": time}

    pprint(data)

    resp = jar.put(data)

    assert resp == 200

    jar_res = jar.get()
    jar_res["dt1"] = str(time)
    data["dt1"] = str(time)
    assert jar_res == data


def test_put_dict_to_lambda_w_encoder():
    jar = Jar(
        lambda_name=lambda_name,
        region=region,
        decoder=datetime_decoder,
        encoder=datetime_encoder,
    )
    time = dt.now()

    data = {"list": [1, 23, 4, 5], "xyz": "xyz", "dt1": time}

    resp = jar.put(data)
    pprint(resp)

    assert resp == 200

    jar_res = jar.get()
    print(jar_res)
    assert jar_res == data


def test_put_data_larger_than_4kb(jar):
    with pytest.raises(botocore.exceptions.ClientError):
        jar.put(list(range(10 ** 3)))


if __name__ == "__main__":
    import logging

    logging.getLogger("awsjar").setLevel(logging.DEBUG)
