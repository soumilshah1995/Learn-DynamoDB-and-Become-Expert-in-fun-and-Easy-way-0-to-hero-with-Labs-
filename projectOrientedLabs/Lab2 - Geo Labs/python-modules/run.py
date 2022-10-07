try:

    import boto3
    import dynamodbgeo
    import uuid
    import os
    from datetime import datetime
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

    from dotenv import load_dotenv

    load_dotenv("../.env")
except Exception as e:
    pass

def unmarshall(dynamo_obj: dict) -> dict:
    """Convert a DynamoDB dict into a standard dict."""
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in dynamo_obj.items()}

def marshall(python_obj: dict) -> dict:
    """Convert a standard dict into a DynamoDB ."""
    serializer = TypeSerializer()
    return {k: serializer.serialize(v) for k, v in python_obj.items()}


class DynamoDBGeoPy(object):
    def __init__(
        self,
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name="",
        table_name="",
        hash_key_length=6,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.table_name = table_name
        self.hash_key_length = hash_key_length

        self.client = boto3.client(
            "dynamodb",
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

        """config"""

        self.config = dynamodbgeo.GeoDataManagerConfiguration(
            self.client, self.table_name
        )
        self.config.hashKeyLength = hash_key_length

        self.config.hashKeyLength = self.hash_key_length
        self.geoDataManager = dynamodbgeo.GeoDataManager(self.config)

    def create_dynamodb_table(self):

        table_util = dynamodbgeo.GeoTableUtil(self.config)
        create_table_input = table_util.getCreateTableRequest()
        table_util.create_table(create_table_input)

        return True

    def insert_data(self, json_data,  lat, lon ):

        json_data = marshall(json_data)

        PutItemInput = {
            "Item": json_data,
            "ConditionExpression": "attribute_not_exists(hashKey)",
        }

        self.geoDataManager.put_Point(
            dynamodbgeo.PutPointInput(
                dynamodbgeo.GeoPoint(lat, lon),
                str(uuid.uuid4()),
                PutItemInput,
            )
        )

        return True

    def radius_search(self, lon=0.0, lat=0.0, radius_meter=47):
        query_reduis_result = self.geoDataManager.queryRadius(
            dynamodbgeo.QueryRadiusRequest(
                dynamodbgeo.GeoPoint(lat, lon),
                int(radius_meter * 2),
                sort=True
            )
        )
        return [unmarshall(item) for item in query_reduis_result]

    def update_items(self):
        pass


def load_data(helper):

    import json

    with open("dunkinDonuts.json", "r") as file:
        data = json.load(file)
        json_data = data.get("data")

        for c,item in enumerate(json_data):
            print("record ", c)
            try:
                json_data = {
                    "city":item.get("city"),
                    "address":item.get("address"),
                    "county":item.get("county"),
                    "url" : item.get("dbi_fee_hr_link"),
                    "data_object":str(item)
                }
                lat = float(item.get("lat"))
                lon = float(item.get("lng"))

                response = helper.insert_data(
                    json_data=json_data,
                    lon=lon,
                    lat=lat
                )
            except Exception as e:
                pass

def main():

    helper = DynamoDBGeoPy(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name=os.getenv("REGION"),
        table_name=os.getenv("TABLE"),
        hash_key_length=3,
    )

    """insert data lat and lon"""
    helper.create_dynamodb_table()
    load_data(helper)


main()
