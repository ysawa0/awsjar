# Jar
Save your data within the Lambda itself, as an environment variable.

This method has **no associated costs** but AWS only allows you to **save up to 4KB of data** in the environment variables.

### Initialization
```
import awsjar

# Cans specify region if testing locally
jar = awsjar.Jar(lambda_name='sams-lambda', region='us-east-1')

# If running the code in Lambda, it will automatically know the proper region it's running in. 
jar = awsjar.Jar(lambda_name='sams-lambda')
```

### Save data
```
data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
jar.put(data)

state = jar.get()
>> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
```

### Serializing data
Jar comes with datetime encoders/decoders for you to use.

It uses the standard library json.dumps and json.loads to serialize data so it's possible to write your own encoder/decoders to serialize your data.

[Here's some instructions](https://www.google.com/search?client=firefox-b-1-ab&ei=FrI2XIe9M-Xk9APIzJbwCw&q=python+json+serialize+data&oq=python+json+serialize+data&gs_l=psy-ab.3..0i22i30l2.51201.51646..51753...0.0..0.183.542.3j2......0....1..gws-wiz.......0i71j0i67j0.5HjqPa8O5YE) 
```
from awsjar import Jar, datetime_decoder, datetime_encoder
from datetime import datetime

jar = Jar(
    lambda_name=lambda_name,
    region=region,
    decoder=datetime_decoder,
    encoder=datetime_encoder,
)
time = datetime.now()

data = {"list": [1, 2, 3], "dt1": time}

jar.put(data)
x = jar.get()
>> {"list": [1, 2, 3], 'dt1': datetime.datetime(2019, 1, 9, 18, 49, 44, 847202)}
```

# Bucket
Save your data on S3.

### Initialization
```
import awsjar

bkt = awsjar.Bucket(bucket='my-bucket', key='state.json')

# Can specify region if you'd like.
bkt = awsjar.Bucket(bucket='my-bucket', key='state.json', region='us-east-1')

# This will pretty print any data saved to S3.
bkt = awsjar.Bucket(bucket='my-bucket', key='state.json', pretty=True)
```

### Save data
```
data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
bkt.put(data)

state = bkt.get()
>> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
```

### Versioning
S3 has an [eventual consistency data model](https://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.html#ConsistencyModel)

This means getting an object immediately after overwriting it may not return the data you expect.

To overcome this, enable [versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/ObjectVersioning.html)

If an S3 Bucket has versioning enabled, Bucket will detect it automatically and fetch the latest version of an object on any `get()` calls.

```
# Check versioning status
bkt.is_versioning_enabled()

# Enable versioning
bkt.enable_versioning()

# Disable versioning
bkt.enable_versioning()
```

### Specifying keys
You can specify the key to override the key that was used in initialization.
```
bkt = aj.Bucket(bucket='my-bucket', key='state.json')
bkt.put(['test'])  # Saved to s3://my-bucket/state.json

data = ['override']
bkt.put(data, key="override.json")  # Saved to s3://my-bucket/override.json

state = bkt.get(key="override.json")
>> ['override']
```

### Serializing data
Similar to Jar
```
from awsjar import Bucket, datetime_decoder, datetime_encoder
from datetime import datetime

bkt = Bucket(
    lambda_name=lambda_name,
    region=region,
    decoder=datetime_decoder,
    encoder=datetime_encoder,
)
time = datetime.now()

data = {"list": [1, 2, 3], "dt1": time}

bkt.put(data)
x = bkt.get()
>> {"list": [1, 2, 3], 'dt1': datetime.datetime(2019, 1, 9, 18, 49, 44, 847202)}
```
