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


def unmarshall(dynamo_obj: dict) -> dict:
    """Convert a DynamoDB dict into a standard dict."""
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in dynamo_obj.items()}


def marshall(python_obj: dict) -> dict:
    """Convert a standard dict into a DynamoDB ."""
    serializer = TypeSerializer()
    return {k: serializer.serialize(v) for k, v in python_obj.items()}


class Datetime(object):
    @staticmethod
    def get_year_month_day():
        """
        Return Year month and day
        :return: str str str
        """
        dt = datetime.now()
        year = dt.year
        month = dt.month
        day = dt.day
        return year, month, day


def flatten_dict(data, parent_key="", sep="_"):
    """Flatten data into a single dict"""
    try:
        items = []
        for key, value in data.items():
            new_key = parent_key + sep + key if parent_key else key
            if type(value) == dict:
                items.extend(flatten_dict(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
        return dict(items)
    except Exception as e:
        return {}


class AWSSQS(object):

    """Helper class to which add functionality on top of boto3 """

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.sqs_client = boto3.resource(
            "sqs",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def get_queue_by_name(self, queue_name=""):
        try:
            queue_name = self.sqs_client.get_queue_by_name(QueueName=queue_name)
            return queue_name
        except Exception as e:
            raise Exception("Error : {}".format(e))

    def __repr__(self):
        return "AWS SQS Helper class "


def lambda_handler(event, context):

    print("event", event)
    print("\n")

    print("Length: {} ".format(len(event["Records"])))

    for record in event["Records"]:

        payload = base64.b64decode(record["kinesis"]["data"])
        de_serialize_payload = json.loads(payload)

        print("de_serialize_payload", de_serialize_payload, type(de_serialize_payload))

        eventName = de_serialize_payload.get("eventName")
        print("eventName", eventName)

        json_data = None

        if eventName.strip().lower() == "INSERT".lower():
            json_data = de_serialize_payload.get("dynamodb").get("NewImage")

        if eventName.strip().lower() == "MODIFY".lower():
            json_data = de_serialize_payload.get("dynamodb").get("NewImage")

        if eventName.strip().lower() == "REMOVE".lower():
            json_data = de_serialize_payload.get("dynamodb").get("OldImage")

        if json_data is not None:
            json_data_unmarshal = unmarshall(json_data)
            json_data_unmarshal["awsRegion"] = de_serialize_payload.pop("awsRegion")
            json_data_unmarshal["eventID"] = de_serialize_payload.pop("eventID")
            json_data_unmarshal["eventName"] = de_serialize_payload.pop("eventName")
            json_data_unmarshal["eventSource"] = de_serialize_payload.pop("eventSource")

            _final_processed_json = flatten_dict(json_data_unmarshal)
            print("_final_processed_json", _final_processed_json)

            """Publish to SQS """
            queue_helper = AWSSQS(
                aws_access_key_id=os.getenv("DEV_AWS_ACCESS_KEY"),
                aws_secret_access_key=os.getenv("DEV_AWS_SECRET_KEY"),
                region_name=os.getenv("DEV_AWS_REGION"),
            )


            data = json.dumps(_final_processed_json, default=str)
            queue = queue_helper.get_queue_by_name(queue_name=os.getenv("SQS_NAME"))
            queue.send_message(MessageBody=data)

    print("****************  ALL SET *********************")
    print("Length: {} ".format(len(event["Records"])))
