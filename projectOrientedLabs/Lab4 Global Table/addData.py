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

AWS_ACCESS_KEY = "XXX"
AWS_SECRET_KEY = "XXXXX"
AWS_REGION_NAME = "us-east-2"

region = ['us-east-1', 'us-west-1']

for _ in range(1, 5):

    random_region = region[random.randint(0, len(region)-1)]

    class UserModel(Model):

        class Meta:
            region = random_region
            table_name = 'myTable'
            aws_access_key_id = AWS_ACCESS_KEY
            aws_secret_access_key = AWS_SECRET_KEY

        email = UnicodeAttribute(hash_key=True)
        userId = UnicodeAttribute(range_key=True)

        region = UnicodeAttribute(null=True)

        first_name = UnicodeAttribute(null=True)
        last_name = UnicodeAttribute(null=True)
        company = ListAttribute()

    faker = Faker()

    UserModel(email=faker.email(),
              userId = ''.join([str(random.randint(1, 200)) for i in range(1, 5)]),
              first_name=faker.first_name(),
              last_name=faker.last_name(),
              company = [faker.company() for i in range(1, 6)],
              region=random_region
              ).save()
    print("""
    Inserting Region: {}

    """.format(random_region))
