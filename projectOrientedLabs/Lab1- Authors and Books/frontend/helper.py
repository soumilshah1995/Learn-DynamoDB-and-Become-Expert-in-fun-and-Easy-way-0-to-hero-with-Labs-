try:
    import uuid
    import os
    import json

    import boto3
    from datetime import datetime

    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
    from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
    from pynamodb.models import Model
    from pynamodb.attributes import *

    from dotenv import load_dotenv
    load_dotenv("../.env")

except Exception as e:
    print("Error", e)


# ----------------------------------------------------------------------------

global TABLE_NAME
TABLE_NAME = f'{os.getenv("TABLE_NAME")}-lab-{os.getenv("LAB_NUMBER")}-team-{os.getenv("TEAM_NUMBER")}'


class AuthorsBooks(Model):
    class Meta:
        table_name = TABLE_NAME
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


class ViewIndex(GlobalSecondaryIndex):

    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = "gs2pk-index"
        projection = AllProjection()
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")

    gs2pk = UnicodeAttribute(hash_key=True)


class CategoriesModel(Model):
    """
    A test model that uses a global secondary index
    """

    class Meta:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        aws_secret_access_key = os.getenv("AWS_SECRET_KEY")
        table_name = TABLE_NAME

    pk = UnicodeAttribute(null=True)
    sk = UnicodeAttribute(null=True)
    author_data_object = MapAttribute(null=True)

    book_title = UnicodeAttribute(null=True)
    book_published_data = UnicodeAttribute(null=True)
    isbn = UnicodeAttribute(null=True)
    total_pages = UnicodeAttribute(null=True)
    book_price = UnicodeAttribute(null=True)
    books_meta_data = MapAttribute(null=True)

    gs1pk = UnicodeAttribute(null=True)
    category = UnicodeAttribute(null=True)
    ttl = NumberAttribute(null=True)

    view_index = ViewIndex()
    gs2pk = UnicodeAttribute(hash_key=True)


def get_sample_books():

    data = []
    for item in AuthorsBooks.scan(AuthorsBooks.pk.startswith("Book#"), limit=20):

        json_data = json.loads(item.to_json())
        thumbnailUrl = json_data.get("books_meta_data", {}).get("thumbnailUrl", None)
        if thumbnailUrl is not None:
            if len(thumbnailUrl) > 6:
                data.append(item.to_json())

    return {
        "data":data
    }


def get_book_from_dynamodb(book):

    hash_table = {}
    for current_object in AuthorsBooks.query(str(book)):
        key = json.loads(current_object.to_json()).get("pk")

        if key not in hash_table:
            hash_table[current_object.pk] = current_object

        if key in hash_table:
            _object = hash_table.get(current_object.pk)
            if current_object.category not in _object.category:
                _object.category = _object.category + "," + current_object.category

    json_data = [value.to_json() for key, value in hash_table.items()]
    return {"data": json_data}


def get_books_categories_from_dynamo_db(category):

    books_data = []

    for book in CategoriesModel.view_index.query(category, limit=20):
        json_data = json.loads(book.to_json()).get("books_meta_data")
        if json_data.get("thumbnailUrl") is not None:
            if len(json_data.get("thumbnailUrl")) > 2:
                books_data.append(book.to_json())

    return {"data": books_data}

def get_categories_auto_complete():
    categories = [  book.sk for book in AuthorsBooks.query("categoryList#") ]
    return {"data": categories}
# -------------------------------------------