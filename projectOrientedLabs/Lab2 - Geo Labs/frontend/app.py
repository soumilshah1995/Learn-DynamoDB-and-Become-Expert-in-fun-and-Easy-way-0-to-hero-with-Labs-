try:
    from flask import Flask, render_template
    import dynamodbgeo
    import uuid
    import os
    import json

    import boto3
    from datetime import datetime
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
    from flask import request
    from dotenv import load_dotenv
    load_dotenv(".env")
except Exception  as e:
    pass


app = Flask(__name__)


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


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = json.loads(dict(request.form).get("data"))
    helper = DynamoDBGeoPy(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name=os.getenv("REGION"),
        table_name=os.getenv("TABLE"),
        hash_key_length=3,
    )

    print("data", data)

    lat = float(data.get("lat"))
    lon = data.get("lon")
    radius = data.get("radius")

    print(f"""
    lat {lat}
    lon {lon}
    radius {radius}

    """)
    radius_value = 70
    if radius != "" or None:
        radius_value = int(radius)

    response = helper.radius_search(lon=lon, lat=lat, radius_meter=radius_value)

    return {"data": response}



if __name__ == '__main__':
    app.run(debug=True, port=5000)