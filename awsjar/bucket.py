import json
import logging

import boto3
from botocore.exceptions import ClientError as BotoClientError

from awsjar.utils import _data_dumper
from awsjar.exceptions import ClientError

log = logging.getLogger(__name__)


class Bucket:
    def __init__(
        self, bucket, key="", region="", encoder=None, decoder=None, pretty=False
    ):
        self.region = region or None
        self._s3 = boto3.resource("s3", region_name=self.region)
        self._cl = boto3.client("s3", region_name=self.region)

        self.key = key
        self.bucket_name = bucket

        self._does_bucket_exist(bucket)
        self.bucket = self._s3.Bucket(bucket)

        if self.is_versioning_enabled():
            self.get = self._get_latest_ver_of_obj
        else:
            self.get = self._get

        if not encoder:
            encoder = str

        indent = 2 if pretty else None

        def _dumps(data):
            return json.dumps(data, default=encoder, indent=indent)

        def _loads(data):
            try:
                return json.loads(data, object_hook=decoder)
            except Exception:
                return data

        self._dumps = _dumps
        self._loads = _loads

    def __str__(self):
        s = f"s3://{self.bucket_name}/{self.key}"
        return s

    def __repr__(self):
        s = f"Bucket(bucket='{self.bucket_name}', key='{self.key}')"
        return s

    def is_versioning_enabled(self):
        ver = self.bucket.Versioning()
        status = ver.status
        if status and status == "Enabled":
            return True
        return False

    def enable_versioning(self):
        ver = self.bucket.Versioning()
        ver.enable()
        self.get = self._get_latest_ver_of_obj

    def disable_versioning(self):
        ver = self.bucket.Versioning()
        ver.suspend()
        self.get = self._get

    def put(self, data, key=""):
        """
        Enocde data into json then put it on S3
        :param data: Either a list or dict
        :return: Boto3 S3 Bucket Resource Object
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.put_object
        """
        k = key or self.key
        data = _data_dumper(data, self._dumps)

        resp = self.bucket.put_object(Body=data, Key=k)
        log.debug(resp)
        return resp

    def _get(self, key=""):
        """ Get and decode stored state from S3.
        If the object does not exist, return an empty dict
        :param key: Key can be specified if you want to
                    fetch something over than self.key
        :return: list or dict
        """
        k = key or self.key

        try:
            obj = self._s3.Object(self.bucket_name, k)
            state = obj.get()
            state = state["Body"].read().decode()
        except BotoClientError as e:
            code = e.response["Error"]["Code"]
            if code == "AccessDenied":
                msg = (
                    f"Received access denied when trying"
                    f" to access S3 object: s3://{self.bucket_name}/{k}"
                )
                raise ClientError(msg)
            elif code == "NoSuchKey":
                return {}
            else:
                raise ClientError(e)
        state = self._loads(state)
        log.debug(state)
        return state

    def _get_latest_ver_of_obj(self, key=""):
        """ Get and decode stored state from S3. If the object does not exist, return an empty dict.
        :param key: Key can be specified if you want to fetch something over than self.key
        :return: list or dict
        """
        k = key or self.key

        obj = self._get_latest_ver_id_of_obj(k)
        log.debug(obj)
        if not obj:
            # If ver obj DNE, return empty dict
            log.info(
                "Latest version of object was not found for s3://{self.bucket_name}/{key}"
            )
            return {}

        try:
            state = obj.get()
        except BotoClientError as e:
            err = e.response["Error"]
            log.info(err)
            msg = "The specified method is not allowed against this resource."
            if err["Code"] == "MethodNotAllowed" and err["Message"] == msg:
                # Object may have been deleted but may still be listed in API call results
                res = self._check_obj_exists(k)
                if not res:
                    # Object does not exist, return empty dict
                    return {}
                else:
                    raise ClientError(e)
            else:
                raise ClientError(e)

        state = state["Body"].read().decode()
        state = self._loads(state)
        log.debug(state)
        return state

    def _check_obj_exists(self, key):
        try:
            self._s3.Object(self.bucket_name, key).load()
        except BotoClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise ClientError(e)
        return True

    def _does_bucket_exist(self, bucket):
        """ Determine if bucket exists and if we have necessary access to it """
        try:
            self._cl.head_bucket(Bucket=bucket)
        except BotoClientError as e:
            err = e.response["Error"]
            if err["Code"] == "403" and err["Message"] == "Forbidden":
                msg = (
                    f"Received forbidden when trying to access S3 bucket: s3://{bucket}"
                )
                raise ClientError(msg)
            elif err["Code"] == "404" and err["Message"] == "Not Found":
                msg = (
                    f"Received not found when trying to access S3 bucket: s3://{bucket}"
                )
                raise ClientError(msg)
            else:
                raise ClientError(e)

    def _get_latest_ver_id_of_obj(self, key=""):
        """ Get latest version id for object.
        :param key: Key can be specified if you want to fetch something over than self.key
        :return: s3.ObjectVersion(bucket_name='', object_key='', id='example-id')
        id will be 'null' for non-versioned objects
        """
        k = key or self.key

        versions = self.bucket.object_versions.filter(Prefix=k)
        latest_ver = [ver for ver in versions if ver.is_latest]
        log.debug(latest_ver)
        if latest_ver:
            return latest_ver[0]
        else:
            return None

    def delete(self, key="", version_id=""):
        """ Delete object. Deletes latest ver of object"""
        k = key or self.key
        obj = self._s3.Object(self.bucket_name, k)
        if version_id:
            resp = obj.delete(VersionId=version_id)
        else:
            resp = obj.delete()
        log.debug(resp)
        return resp


if __name__ == "__main__":
    # logging.basicConfig()
    # log.setLevel(logging.DEBUG)
    # b = Bucket(bucket="awsjar-testing-regular-bucket", key="object-with-no-versions")
    # b.put({"testing": 1234})
    # b.delete()
    # x = b.get()
    # print("get", x)
    # x = b.is_versioning_enabled()
    # print(x)
    BotoClientError('asdf', {})