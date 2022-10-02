try:
    import json
    import json
    import boto3
    import base64
    import os
    import datetime
    import uuid
    from datetime import datetime
    from pynamodb.models import Model
    from pynamodb.attributes import *
except Exception as e:
    print("Error : {} ".format(e))


class LinkedinStats(Model):
    class Meta:
        table_name = os.getenv("TABLE_NAME_STATS")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    pk = UnicodeAttribute(hash_key=True,)
    sk = UnicodeAttribute(range_key=True)

    likes = UnicodeAttribute(null=True)
    comment = UnicodeAttribute(null=True)


def likes_stats_update_for_post(json_data):

    pk = json_data.get("pk")

    sk = json_data.get("sk")

    post_id = json_data.get("post_user_likes_gsi")

    if "like_id#" in pk:
        found = False

        for items in LinkedinStats.query(post_id):
            if "like_id#" in items.pk:
                found = True
                break

        """This posts meta data is not there initialize to zero """
        if found == False:
            LinkedinStats(pk=post_id, likes=0, comment=0)
        else:
            for items in LinkedinStats.query(post_id):
                items.likes = items.likes + 1
                items.save()
                break


def comments_stats_update_for_post(json_data):

    pk = json_data.get("pk")
    sk = json_data.get("sk")
    post_id = json_data.get("post_users_comments_gsi")

    if "comment_id#" in pk:
        found = False

        for items in LinkedinStats.query(post_id):
            if "comment_id#" in items.pk:
                found = True
                break

        """This posts meta data is not there initialize to zero """
        if found == False:
            LinkedinStats(pk=post_id, likes=0, comment=0)
        else:
            for items in LinkedinStats.query(post_id):
                items.comment = items.comment + 1
                items.save()
                break


def stats(event, context):
    """

    Stats Logic
    """
    messages = event.get("Records", [])

    for message in messages:
        print("sqs message ", message)

    return "ok"
