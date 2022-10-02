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
    from dotenv import load_dotenv
    load_dotenv(".env")
except Exception as e:
    print("Error : {} ".format(e))


class LinkedinStats(Model):
    class Meta:
        table_name = os.getenv("TABLE_NAME_STATS")
        aws_access_key_id = os.getenv("DEV_AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("DEV_AWS_SECRET_KEY")

    pk = UnicodeAttribute(hash_key=True,)
    sk = UnicodeAttribute(range_key=True)

    likes = UnicodeAttribute(null=True)
    comment = UnicodeAttribute(null=True)

def likes_stats_update_for_post(json_data):

    pk = json_data.get("pk")
    sk = json_data.get("sk")
    post_id = json_data.get("post_user_likes_gsi")


    if "like#" in pk:
        found = False

        for items in LinkedinStats.query(str(post_id)):
            print("items", items.to_json())

            if "post_id#" in items.pk:
                found = True
                break

        """This posts meta data is not there initialize to zero """

        if found == False:
            likes=  str(0)
            comment = str(0)
            LinkedinStats(pk=post_id, sk=post_id ,likes=likes, comment=comment).save()

        else:
            for items in LinkedinStats.query(post_id):
                if json_data.get("eventName").lower() == "INSERT".lower():
                    items.likes = str(int(items.likes) + 1)
                    items.save()
                    break
                if json_data.get("eventName").lower() == "REMOVE".lower():
                    items.likes = str(int(items.likes) - 1)
                    items.save()
                    break

def comments_stats_update_for_post(json_data):

    pk = json_data.get("pk")
    sk = json_data.get("sk")
    post_id = json_data.get("post_users_comments_gsi")

    print(f"""
     pk {pk}
     sk {sk}
     post_id {post_id}
    """)

    if "comment_id#" in pk:
        found = False

        for items in LinkedinStats.query(str(post_id)):
            print("******************")
            print("item", items)
            print(items.pk)
            print(items.to_json())
            print("******************")

            if "comment_id#" in pk:
                found = True
                break

        """This posts meta data is not there initialize to zero """
        print("found **********",found)

        if found == False:
            likes= str(0)
            comment = str(0)
            LinkedinStats(pk=post_id, sk=post_id,likes=likes, comment=comment).save()

        else:
            for items in LinkedinStats.query(post_id):
                if json_data.get("eventName").lower() == "INSERT".lower():
                    items.comment = str(int(items.comment) + 1)
                    items.save()
                    break
                if json_data.get("eventName").lower() == "REMOVE".lower():
                    items.comment = str(int(items.comment) - 1)
                    items.save()
                    break

def stats(event=None, context=None):
    """

    Stats Logic
    """
    messages = event.get("Records", [])

    for message in messages:
        json_data = json.loads(message.get("body"))

        if "like#" in json_data.get("pk"):
            print(messages)
            print("inside like method ")
            likes_stats_update_for_post(json_data)

        if "comment_id#" in json_data.get("pk"):
            print("inside comment method ")
            print(json.dumps(json_data, indent=3))
            comments_stats_update_for_post(json_data)

        print("sqs message ", message)

    return "ok"



"""
TEST PAYLAOD 

    messages=[
        {
            "messageId":"b9c292bc-ac60-450d-8e7e-5d785e104ad5",
            "receiptHandle":"AQEBJmVhi0r1LTHCsiosVRXkY0GOF8csYfCXTe5XXjz1NEZpmide+9Aitaf3k6d24KED8xLRVjtTT8hcmhQVNIH3JKxCMifxirDmdVPzF/i7kE50sHw5olzlkS4K9hag3OD3YFU2xk8AdyWU68+HKuj/lyKv5DvfgNKMzdIUPivdwc14hL0mXyz4Dw636+aT7/h+f9q6d90OL4MveA7M3Unuee5JNyXPb0C7hhRaqhojShJ0bdoLTfFTP9KGfHbYyIKSUZVGXI8Vc2ixItqM+ywh5I8kqYyLZfHKJ/XoN+tIRVDuYXnBKQVgiJ9hsjSDT3Ti36D3BRVtrhjLd0Whd8ONrFv8o3DW7f9louZlOdbZTlELRdCFq8tzQSl2CPYNn4WAnemcKqbIpkOyYa1+73GFiQ==",
            "body":"{\"comment_date\": \"2020-12-10\", \"comment_text\": \"Around factor safe cup.\\nLot bit religious thank activity husband. Chance beyond now occur. Picture hundred employee.\\nEnergy glass teach prove site. Firm reach upon society single dream.\", \"sk\": \"comment_id#1fb8b214-d617-47d1-94e1-22e4ea23686b#user#user#99fc7c29-c44b-46ea-8365-e384a703acbc\", \"user_post_gsi\": \"user#99fc7c29-c44b-46ea-8365-e384a703acbc\", \"pk\": \"comment_id#1fb8b214-d617-47d1-94e1-22e4ea23686b\", \"post_users_comments_gsi\": \"post_id#30dfb3f7-3007-4038-9e54-b51880f0e421\", \"awsRegion\": \"us-east-1\", \"eventID\": \"165d1f32-3acd-473c-a545-afe42a48e9f0\", \"eventName\": \"INSERT\", \"eventSource\": \"aws:dynamodb\"}",
            "attributes":{
                "ApproximateReceiveCount":"1",
                "SentTimestamp":"1664736570845",
                "SenderId":"AIDA4TYY74BHXEUVFGSSE",
                "ApproximateFirstReceiveTimestamp":"1664736570846"
            },
            "messageAttributes":{

            },
            "md5OfBody":"0b2557fcd88b03dcdb6b959247e42174",
            "eventSource":"aws:sqs",
            "eventSourceARN":"arn:aws:sqs:us-east-1:867098943567:linkedin_stats_queue",
            "awsRegion":"us-east-1"
        }
    ]
"""
