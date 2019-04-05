import os
import sys
import time
from datetime import datetime

import pytest

from awsjar import Bucket, datetime_decoder, datetime_encoder
from awsjar.exceptions import ClientError

ver = sys.version_info

if ver.major == 3 and ver.minor == 7:
    pass
elif ver.major == 3 and ver.minor == 6:
    if os.getenv("travis_ci_job", "") == "true":
        time.sleep(120)

ver_bucket = "awsjar-testing-versioning"
key = "awsjar-integration-tests"
region = ""
s3_bucket = "awsjar-testing-regular-bucket"

time_now = datetime.now()

d1_test_put_dict = {"list": [1, 23, 4, 5], "xyz": "xyz", "dt1": time_now}
d2_test_put_lists = [1, 2, 3, 4, 5, {"test": "example"}, ["a", "b", {"test": "test"}], {"dt1": time_now}]

int_data = 123412343959235182312759283518273923
float_data = 12341234395923518231.2759283518273923
neg_data = -123412343959235182312759283518273923
zero = 0
str_data = "1242u51234usdfhashf1u23hajsd" * 10


@pytest.fixture
def bucket():
    return Bucket(key=key, region=region, bucket=s3_bucket)


@pytest.mark.parametrize("data", [d1_test_put_dict, d2_test_put_lists])
def test_put_dict(bucket, data):
    resp = bucket.put(data)
    assert resp.bucket_name == s3_bucket


def test_put_dict_w_override(bucket):
    data = {"abc": [1, 2, 3]}
    bucket.put(data, key="override.json")
    res = bucket.get(key="override.json")
    assert data == res


@pytest.mark.parametrize("data", [d1_test_put_dict, d2_test_put_lists])
def test_put_list_to_lambda_then_get(bucket, data):
    resp = bucket.put(data)

    assert resp.bucket_name == s3_bucket

    bucket_res = bucket.get()

    if isinstance(bucket_res, list):
        data[7]["dt1"] = str(data[7]["dt1"])
    elif isinstance(bucket_res, dict):
        data["dt1"] = str(data["dt1"])

    assert bucket_res == data


@pytest.mark.parametrize("data", [d1_test_put_dict])
def test_put_dict_to_lambda_w_encoder(data):
    bucket = Bucket(key=key, region=region, bucket=s3_bucket, decoder=datetime_decoder, encoder=datetime_encoder)

    resp = bucket.put(data)

    assert resp.bucket_name == s3_bucket

    bucket_res = bucket.get()
    assert bucket_res == data


def test_bucket_does_not_exist():
    with pytest.raises(ClientError):
        Bucket(bucket="example-awsjar-non-existent-bucket-353412312513", key=key)


def test_access_denied_for_bucket():
    with pytest.raises(ClientError):
        Bucket(bucket="example")


def test_access_denied_for_obj():
    with pytest.raises(ClientError):
        bkt = Bucket(bucket="awsjar-testing-forbidden-objects", key="forbidden-object")
        bkt.get()


def test_get_ver_id_of_non_ver_object():
    """ Non versioned objects have id of null """
    bkt = Bucket(bucket="awsjar-testing-regular-bucket", key="object-with-no-versions")
    ver_id = bkt._get_latest_ver_id_of_obj().id
    assert ver_id == "null"


def test_is_versioning_enabled(bucket):
    bkt = Bucket(bucket=ver_bucket)
    res = bkt.is_versioning_enabled()
    assert res

    bkt = Bucket(bucket=s3_bucket)
    bkt.disable_versioning()
    res = bkt.is_versioning_enabled()
    assert not res


def test_get_latest_ver_id_of_obj():
    bkt = Bucket(bucket=ver_bucket, key="test_get_latest_ver_id_of_obj_dont_edit")
    v = bkt._get_latest_ver_id_of_obj()
    assert v.id == "l889rYbHoTeSGRffAv_epr_MGgPwBRW4"


def test_get_latest_ver_of_obj():
    key = "test_get_latest_ver.json"
    bucket = Bucket(bucket=ver_bucket, key=key)
    i = 0
    while i < 5:
        data = list(range(0, i ** 2))
        data = {"data": data}
        bucket.put(data)
        state = bucket.get()
        assert data == state
        i += 1


def test_get_latest_ver_of_obj_errors_for_invalid_key():
    bkt = Bucket(bucket=ver_bucket, key="non-existent-object")
    v = bkt._get_latest_ver_id_of_obj()
    assert v is None


def test_obj_does_not_exist():
    bucket = Bucket(bucket=s3_bucket, key="does_not_exist")
    state = bucket.get()
    assert state == {}


def test_ver_obj_does_not_exist():
    bucket = Bucket(bucket=ver_bucket, key="does_not_exist")
    state = bucket.get()
    assert state == {}


def test_str():
    bucket = Bucket(bucket=s3_bucket, key="does_not_exist")
    assert str(bucket) == "s3://awsjar-testing-regular-bucket/does_not_exist"


def test_repr():
    bucket = Bucket(bucket=s3_bucket, key="does_not_exist")
    assert repr(bucket) == "Bucket(bucket='awsjar-testing-regular-bucket', key='does_not_exist')"


@pytest.mark.parametrize("data", [int_data, str_data, float_data, neg_data, zero])
def test_put_regular_data(bucket, data):
    bucket.put(data)
    state = bucket.get()
    assert state == data


@pytest.mark.parametrize("data", [d1_test_put_dict, d2_test_put_lists])
def test_put_dict_w_pretty(data):
    bkt = Bucket(key=key, region=region, bucket=s3_bucket, pretty=True)
    bkt.put(data)
    state = bkt.get()
    assert data == state


if __name__ == "__main__":
    pass
