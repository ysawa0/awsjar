# import json
# from datetime import datetime
# from unittest.mock import Mock
#
# import pytest
#
# from awsjar import Bucket, datetime_decoder, datetime_encoder
#
#
# key = "awsjar-integration-tests"
# region = ""
# s3_bucket = "awsjar-testing-regular-bucket"
#
# time_now = datetime.now()
#
#
# d1_test_put_dict = {"list": [1, 23, 4, 5], "xyz": "xyz", "dt1": time_now}
# d2_test_put_lists = [
#     1,
#     2,
#     3,
#     4,
#     5,
#     {"test": "example"},
#     ["a", "b", {"test": "test"}],
#     {"dt1": time_now},
# ]
#
#
# @pytest.fixture
# def bucket():
#     bkt = Bucket(key=key, region=region, bucket=s3_bucket)
#     bkt.bucket = Mock()
#     resp_mock = Mock()
#     resp_mock.bucket_name = s3_bucket
#     bkt.bucket.put_object.return_value = resp_mock
#     return bkt
#
#
# @pytest.mark.parametrize("data", [d1_test_put_dict, d2_test_put_lists])
# def test_put_dict_to_lambda(bucket, data):
#     resp = bucket.put(data)
#     assert resp.bucket_name == s3_bucket
#
#
# @pytest.mark.parametrize("data", [d1_test_put_dict, d2_test_put_lists])
# def test_put_list_to_lambda_then_get(bucket, data):
#     resp = bucket.put(data)
#
#     assert resp.bucket_name == s3_bucket
#
#     print(bucket)
#
#     bucket.bucket.download_file.return_value = {}
#
#     with open("/tmp/bucket.tmp", "w") as tmp:
#         t = json.dumps(data, default=str)
#         tmp.write(t)
#
#     bucket_res = bucket.get()
#
#     if isinstance(bucket_res, list):
#         data[7]["dt1"] = str(data[7]["dt1"])
#     elif isinstance(bucket_res, dict):
#         data["dt1"] = str(data["dt1"])
#
#     assert bucket_res == data
#
#
# @pytest.mark.parametrize("data", [d1_test_put_dict])
# def test_put_dict_to_lambda_w_encoder(data):
#     bkt = Bucket(
#         key=key,
#         region=region,
#         bucket=s3_bucket,
#         decoder=datetime_decoder,
#         encoder=datetime_encoder,
#     )
#
#     bkt.bucket = Mock()
#     resp_mock = Mock()
#     resp_mock.bucket_name = s3_bucket
#     bkt.bucket.put_object.return_value = resp_mock
#
#     resp = bkt.put(data)
#
#     assert resp.bucket_name == s3_bucket
#
#     bkt.bucket.download_file.return_value = {}
#
#     with open("/tmp/bucket.tmp", "w") as tmp:
#         t = json.dumps(data, default=str)
#         tmp.write(t)
#
#     bucket_res = bkt.get()
#     assert bucket_res == data
#
#
# if __name__ == "__main__":
#     pass
