try:
    import os
    import boto3
    from pynamodb.models import Model
    from pynamodb.attributes import *

    from dotenv import load_dotenv
    load_dotenv("../.env")

except Exception as e:
    print("Error : {}".format(e))


class AuthorsBooks(Model):
    class Meta:
        _ = f'{os.getenv("TABLE_NAME")}-lab-{os.getenv("LAB_NUMBER")}-team-{os.getenv("TEAM_NUMBER")}'
        table_name = _
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
    author_data_object = MapAttribute(null=True)

    book_title = UnicodeAttribute(null=True)
    book_published_data = UnicodeAttribute(null=True)
    isbn = UnicodeAttribute(null=True)
    total_pages = UnicodeAttribute(null=True)
    book_price = UnicodeAttribute(null=True)
    books_meta_data = MapAttribute(null=True)


    gs1pk = UnicodeAttribute(null=True)
    category = UnicodeAttribute(null=True)

    gs2pk = UnicodeAttribute(null=True)
    ttl = NumberAttribute(null=True)

