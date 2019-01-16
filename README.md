# AWS Jar
[![PyPI version](https://badge.fury.io/py/awsjar.svg)](https://badge.fury.io/py/awsjar)
[![Downloads](https://pepy.tech/badge/awsjar/month)](https://pepy.tech/project/awsjar)
[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

<p align="center">
  <img src="https://raw.githubusercontent.com/ysawa0/awsjar/master/docs/logo.png" alt="Jar Logo" width="45%" height="45%"/>
</p>


[Jar](https://github.com/ysawa0/awsjar) makes it easy to save the state of your AWS Lambda functions.

The data (either a dict or list) can be saved within the Lambda itself as an environment variable or on S3.

## Install
```
pip install awsjar
```

## Examples
### Increment a sum with every invocation
```
import awsjar

def lambda_handler(event, context):
    jar = awsjar.Jar(context.function_name)
    data = jar.get()  # Will return an empty dict if state does not already exist.

    s = data.get("sum", 0)
    data["sum"] = s + 1

    jar.put(data)
    
    return data
```
### Run a health check against your website
```
import awsjar
import requests

# Set a CloudWatch Event to run this Lambda every minute.
def lambda_handler(event, context):
    jar = awsjar.Jar(context.function_name)
    data = jar.get()  # Will return an empty dict if state does not already exist.
    
    last_status_code = data.get("last_status_code", 200)
    
    result = requests.get('http://example.com')
    cur_status_code = result.status_code
    
    if last_status_code != 200 and cur_status_code != 200:
        print('Website might be down!')

    jar.put({'last_status_code': cur_status_code})
```
### Save data to S3

```
import awsjar

# Save your data to an S3 object - s3://my-bucket/state.json 
bkt = awsjar.Bucket('my-bucket', key='state.json')

data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
bkt.put(data)

state = bkt.get()
>> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
```

## Docs
[User Guide](https://github.com/ysawa0/awsjar/blob/master/docs/guide.md)

## Contributing

Please see the [contributing guide](CONTRIBUTING.md) for more specifics.

## Contact / Support

Please use the [Issues](https://github.com/ysawa0/awsjar/issues)

Any suggestions / feedback is also welcome! Email me at: yukisawa@gmail.com

## License

Distributed under the Apache License 2.0. See [`LICENSE`](LICENSE) for more information.
