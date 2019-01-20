from datetime import datetime as dt

import pytest
import botocore
from pprintpp import pprint

from awsjar import Jar, datetime_decoder, datetime_encoder
from awsjar.exceptions import ClientError

lambda_name = "jar-integration-test"
region = "us-east-1"


@pytest.fixture(params=[False, True])
def jar(request):
    return Jar(lambda_name=lambda_name, region=region, compression=request.param)


def test_init_jar_for_lambda_w_no_env_vars(jar):
    jar.delete()
    data = jar.get()
    assert data == {}
    data = {'test': 1}
    jar.put(data)
    assert jar.get() == data


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


def test_put_dict_to_lambda_w_encoder(jar):
    jar = Jar(
        lambda_name=jar.lambda_name,
        region=jar.region,
        decoder=datetime_decoder,
        encoder=datetime_encoder,
        compression=jar.compression,
    )
    time = dt.now()

    data = {"list": [1, 23, 4, 5], "xyz": "xyz", "dt1": time}

    resp = jar.put(data)
    pprint(resp)

    assert resp == 200

    jar_res = jar.get()
    print(jar_res)
    assert jar_res == data


def test_put_data_larger_than_4kb_w_no_compress(jar):
    jar.compression = False
    with pytest.raises(botocore.exceptions.ClientError):
        jar.put(list(range(1000)))


def test_put_5kb_data_w_compress(jar):
    jar.compression = True
    data = list(range(1000))
    jar.put(data)
    res = jar.get()
    assert data == res


def test_put_8kb_data_w_compress(jar):
    jar.compression = True
    with pytest.raises(botocore.exceptions.ClientError):
        data = list(range(1500))
        jar.put(data)


def test_go_from_compressed_to_uncompressed(jar):
    jar.compression = True
    data = {"test": 1}
    jar.put(data)

    jar.compression = False

    res = jar.get()
    assert res == data


def test_go_from_uncompressed_to_compressed(jar):
    jar.compression = False
    data = {"test": 1}
    jar.put(data)

    jar.compression = True

    res = jar.get()
    assert res == data


if __name__ == "__main__":
    import logging
    logging.getLogger("awsjar").setLevel(logging.DEBUG)
    j = Jar(lambda_name=lambda_name, region=region, compression=True)
    # test_go_from_compressed_to_uncompressed(j)
    # test_go_from_uncompressed_to_compressed(j)
    test_init_jar_for_lambda_w_no_env_vars(j)
