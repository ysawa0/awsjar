import json
import logging
import binascii

import boto3

from awsjar.utils import _data_dumper, _compress, _decompress, _convert_str_to_number
from awsjar.exceptions import ClientError

log = logging.getLogger(__name__)


class Jar:
    def __init__(
        self, lambda_name, region="", encoder=None, decoder=None, compression=False
    ):
        self.region = region or None
        self.cl = boto3.client("lambda", region_name=self.region)

        self.lambda_name = lambda_name
        self.compression = compression

        if not encoder:
            encoder = str

        def _dumps(data):
            return json.dumps(data, default=encoder)

        def _loads(data):
            try:
                return json.loads(data, object_hook=decoder)
            except Exception:
                return _convert_str_to_number(data)

        self._dumps = _dumps
        self._loads = _loads

    def get(self):
        """ Get state stored in Lambda environment variable."""
        env_vars = self._fetch_lambda_env_vars(self.lambda_name)
        data = env_vars.get("jar", "")

        if not data:
            return {}

        try:
            data = _decompress(data)  # Decompress bytes into string
        except Exception:
            pass

        data = self._loads(data)
        log.debug(data)
        return data

    def put(self, data):
        """ Store state as Lambda environment variable under key 'jar'."""
        log.debug(data)
        data = _data_dumper(data, self._dumps)

        if self.compression:
            data = _compress(data)  # Compress json using zlib

        env_vars = self._fetch_lambda_env_vars(self.lambda_name)
        env_vars["jar"] = data

        resp = self._update_function_config(self.lambda_name, env_vars)
        log.debug(resp)

        resp = resp.get("ResponseMetadata", {}).get("HTTPStatusCode", "")
        return resp

    def _fetch_lambda_env_vars(self, lambda_func_name):
        """ Fetch all Lambda environment variables."""
        resp = self.cl.get_function_configuration(FunctionName=lambda_func_name)
        if "Environment" not in resp:
            # No env vars exist yet, return empty dict
            return {}

        try:
            env_vars = resp["Environment"]["Variables"]
        except KeyError:
            msg = f"Error getting Lambda env var, boto3 resp: {resp}"
            raise ClientError(msg)

        return env_vars

    def _update_function_config(self, func_name, env_vars):
        """ Update the Lambda with new enviroment variables """
        # import sys
        #
        # tstr = str(env_vars).replace('"', '\\"')
        # size = sys.getsizeof(tstr)
        #
        # print("sizeof str:", sys.getsizeof(tstr))
        # print("len    str:", len(tstr))  # max 4102
        #
        # assert size < 4151, "data size must be smaller than 4KB"

        resp = self.cl.update_function_configuration(
            FunctionName=func_name, Environment={"Variables": env_vars}
        )
        return resp

    def delete(self):
        env_vars = {}
        self._update_function_config(self.lambda_name, env_vars)


if __name__ == "__main__":
    lambda_name = "jar-integration-test"
    region = "us-east-1"
    j = Jar(lambda_name=lambda_name, region=region)
    x = j.get()
    print(x)

    data = {"123": "abc", "a": 123}
    j.put(data)

    x = j.get()

    # import zlib
    #
    # teststr = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus
    # pretium justo eget elit eleifend, et dignissim quam eleifend. Nam vehicula nisl
    # posuere velit volutpat, vitae scelerisque nisl imperdiet. Phasellus dignissim,
    # dolor amet."""
    #
    # cmpstr = zlib.compress(teststr.encode('utf-8'))
