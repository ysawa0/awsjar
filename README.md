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
### Save data inside a Lambda environment variable
```
import awsjar

# Save your data with the Lambda itself, as an Environment Variable.
jar = awsjar.Jar(lambda_name='sams-lambda')
data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
jar.put(data)

state = jar.get()
>> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}

```
### Save data on an S3 Bucket

```
import awsjar

# Save your data to an S3 object - s3://my-bucket/state.json 
bkt = awsjar.Bucket(bucket='my-bucket', key='state.json')

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

Please use the [Issues](https://github.com/ysawa0/awsjar/issues) page

## License

Distributed under the Apache License 2.0. See [`LICENSE`](LICENSE) for more information.
