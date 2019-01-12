AWS Jar
=========
`Jar
<https://github.com/ysawa0/awsjar/>`_ makes it easy to save the state of your AWS Lambda functions.
The data (either a dict or list) can be saved within the Lambda itself as an environment variable or on S3.

Install
-------
.. code-block:: python

    pip install awsjar

Examples
--------------

Save state with Jar inside a Lambda environment variable
--------------------------------------------------------

.. code-block:: python

    import awsjar

    # Save your data with the Lambda itself, as an Environment Variable.
    jar = awsjar.Jar(lambda_name='sams-lambda')
    data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
    jar.put(data)

    state = jar.get()
    >> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}

Save state with Bucket on an S3 bucket
----------------------------------------

.. code-block:: python

    import awsjar

    # Save your data to an S3 object - s3://my-bucket/state.json
    bkt = awsjar.Bucket(bucket='my-bucket', key='state.json')

    data = {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}
    bkt.put(data)

    state = bkt.get()
    >> {'num_acorns': 50, 'acorn_hideouts': ['tree', 'lake', 'backyard']}

Docs
----
`User Guide
<https://github.com/ysawa0/awsjar/blob/master/docs/guide.md>`_