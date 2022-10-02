try:
    import json
    import json
    import boto3
    import base64
    import os
    import datetime
    import uuid
    from datetime import datetime
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
except Exception as e:
    print("Error : {} ".format(e))


def stats(event, context):
    """

    Stats Logic
    :param event:
    :param context:
    :return:
    """

