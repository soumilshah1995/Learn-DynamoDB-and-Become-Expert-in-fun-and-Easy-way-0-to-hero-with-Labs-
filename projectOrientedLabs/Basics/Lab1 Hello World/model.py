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

global TABLE_NAME
TABLE_NAME = f'{os.getenv("TABLE_NAME")}-lab-{os.getenv("LAB_NUMBER")}-team-{os.getenv("TEAM_NUMBER")}'


class UserModel(Model):
    class Meta:
        table_name = TABLE_NAME
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    user_id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute(range_key=True)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)


def load_data():

    for i in range(1, 100):
        response = UserModel(
            user_id=random.randint(1, 8).__str__(),
            order_id=random.randint(1, 100).__str__(),
            first_name=faker.first_name().__str__(),
            last_name=faker.last_name().__str__(),
        ).save()
        print(response)


def bulk_inserts():

    bulk_items = [
        UserModel(
            user_id=random.randint(1, 8).__str__(),
            order_id=random.randint(1, 100).__str__(),
            first_name=faker.first_name().__str__(),
            last_name=faker.last_name().__str__(),
        )
        for i in range(1, 100)
    ]

    with UserModel.batch_write() as batch:
        for item in bulk_items:
            batch.save(item)

def clean_table():
    for x in UserModel.scan():
        x.delete()


def query():

    print("*" * 50)
    for user in UserModel.query("1"):
        print(user.to_json())

    print("*" * 50)
    for user in UserModel.query("1", UserModel.order_id.between("20", "40")):
        print(user.to_json())


if __name__ == "__main__":
    load_data()



