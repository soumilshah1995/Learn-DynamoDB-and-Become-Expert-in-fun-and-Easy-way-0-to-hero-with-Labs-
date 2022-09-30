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
import uuid
from dotenv import load_dotenv

load_dotenv(".env")


class Linkedin(Model):
    class Meta:
        table_name = os.getenv("TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    pk = UnicodeAttribute(hash_key=True,)
    sk = UnicodeAttribute(range_key=True)
    user_object = MapAttribute(null=True)

    """*************Entity Post *****************"""
    post_text = UnicodeAttribute(null=True)
    post_date = UnicodeAttribute(null=True)

    comment_text = UnicodeAttribute(null=True)
    comment_date = UnicodeAttribute(null=True)

    user_post_gsi = UnicodeAttribute(null=True)
    post_users_comments_gsi = UnicodeAttribute(null=True)
    post_user_likes_gsi = UnicodeAttribute(null=True)

def generate_users():
    faker = Faker()
    _ = faker.simple_profile()
    _['user_id'] = uuid.uuid4().__str__()
    _['birthdate'] = _.pop("birthdate").__str__()
    return _

def generate_posts():
    faker = Faker()
    _={}
    _["post_text"] = faker.text()
    _['post_id'] = uuid.uuid4().__str__()
    _['post_date'] = faker.date()
    return _

def generate_comment():
    faker = Faker()
    _={}
    _["comment_text"] = faker.text()
    _['comment_id'] = uuid.uuid4().__str__()
    _['comment_date'] = faker.date()
    return _

def generate_likes():
    faker = Faker()
    _={}
    _["like_text"] = faker.text()
    _['like_id'] = uuid.uuid4().__str__()
    _['like_date'] = faker.date()
    return _

def clean_table():
    for x in Linkedin.scan():
        x.delete()

def main():

    clean_table()

    total_users = 4
    total_posts_range = 2
    total_comments_on_posts = 2
    total_likes_on_posts = 2

    for user in range(1, total_users):
        user = generate_users()
        response = Linkedin(
            pk=f"user#{user.get('user_id')}",
            sk=f"user#{user.get('user_id')}",
            user_object= user
        ).save()
        print(f"generating User : user#{user.get('user_id')}")

        for post in range(1, total_posts_range):

            post = generate_posts()

            response = Linkedin(
                pk=f"post_id#{post.get('post_id')}",
                sk=f"post_id#{post.get('post_id')}#user#{post.get('user_id')}",
                post_text=post.get("post_text"),
                post_date=post.get("post_date"),
                user_post_gsi=f"user#{user.get('user_id')}"
            ).save()
            print(f"generating Post post_id#{post.get('post_id')}  for User  : post_id#{post.get('user_id')}   ")

    users = [user.pk for user in Linkedin.scan(Linkedin.pk.startswith("user#"))]
    posts = [user.pk for user in Linkedin.scan(Linkedin.pk.startswith("post_id#"))]

    for post in posts:

        for user in range(1, total_comments_on_posts):

            random_user = random.choice(users)
            comment = generate_comment()

            response = Linkedin(
                            pk=f"comment_id#{comment.get('comment_id')}",
                            sk=f"comment_id#{comment.get('comment_id')}#user#{random_user}",
                            comment_text=comment.get("comment_text"),
                            comment_date=comment.get("comment_date"),
                            user_post_gsi=f"{random_user}",
                            post_users_comments_gsi=f"{post}",

                        ).save()
            print(f"generating comments {comment.get('comment_id')} on posts :{posts}")

        for user in range(1, total_likes_on_posts):
            random_user = random.choice(users)
            like = generate_likes()
            response = Linkedin(
                pk=f"like#{like.get('like_id')}",
                sk=f"like#{like.get('like_id')}#user#{random_user}",
                user_post_gsi=f"{random_user}",
                post_user_likes_gsi=f"{post}",

            ).save()
            print(f"generating likes {like.get('like_id')} on posts :{posts}")

main()