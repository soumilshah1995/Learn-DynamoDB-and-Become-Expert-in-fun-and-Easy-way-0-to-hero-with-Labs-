import os
import boto3
import json
from faker import Faker
import random
import pynamodb.attributes as at
import datetime
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import *
from dotenv import load_dotenv
load_dotenv(".env")


faker = Faker()

class UserModel(Model):
    class Meta:
        table_name = os.getenv("TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    user_id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute(range_key=True)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)

def main():

    for i in range(1, 100):
        response = UserModel(
            user_id=random.randint(1, 8).__str__(),
            order_id=random.randint(1, 100).__str__(),
            first_name=faker.first_name().__str__(),
            last_name=faker.last_name().__str__(),

        ).save()
        print(response)


def query():
    for user in UserModel.query("2", UserModel.order_id.between("20", "40")):
        print(user.to_json())


if __name__ == "__main__":
    main()