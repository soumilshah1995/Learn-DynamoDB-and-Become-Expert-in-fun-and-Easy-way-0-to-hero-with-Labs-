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
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import NumberAttribute

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
    product_id = UnicodeAttribute(range_key=True)
    product_name = UnicodeAttribute(null=True)
    product_desc = UnicodeAttribute(null=True)


class ViewIndex(GlobalSecondaryIndex):

    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = 'product_id-user_id-index'
        projection = AllProjection()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    user_id = UnicodeAttribute(range_key=True)
    product_id = UnicodeAttribute(hash_key=True)


class TestModel(Model):
    """
    A test model that uses a global secondary index
    """
    class Meta:
        table_name =TABLE_NAME
    user_id = UnicodeAttribute(range_key=True)
    product_id = UnicodeAttribute(hash_key=True)
    product_name = UnicodeAttribute(null=True)
    product_desc = UnicodeAttribute(null=True)
    view_index = ViewIndex()



def populate_tables():

    for i in range(1, 100):
        response = UserModel(
            user_id=random.randint(1, 5).__str__(),
            product_id=random.randint(1, 10).__str__(),
            product_name="product#{}".format(random.randint(1, 10),
            product_desc="some info"),

        ).save()
        print(response)


def query_pk_sk():
    for user in UserModel.query("2"):
        print(user.to_json())


def query_gsi():
    for user in TestModel.view_index.query("2"):
        print(user.to_json())

if __name__ == "__main__":

    #populate_tables()
    query_pk_sk()
    print("*"*55)
    query_gsi()