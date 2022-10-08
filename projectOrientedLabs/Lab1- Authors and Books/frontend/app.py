try:
    from flask import Flask, render_template
    import dynamodbgeo
    import uuid
    import os
    import json

    import boto3
    from datetime import datetime
    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
    from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
    from flask import request

    from dotenv import load_dotenv
    load_dotenv("../.env")

    from pynamodb.models import Model
    from pynamodb.attributes import *

except Exception  as e:
    pass

app = Flask(__name__)
global TABLE_NAME
TABLE_NAME = f'{os.getenv("TABLE_NAME")}-lab-{os.getenv("LAB_NUMBER")}-team-{os.getenv("TEAM_NUMBER")}'

print("TABLE_NAME", TABLE_NAME)

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
        index_name = 'gs2pk-index'
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
        table_name =  TABLE_NAME

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



@app.route('/', methods=["GET", "POST"])
def home():
    book_data = [book.to_json() for book in AuthorsBooks.scan(AuthorsBooks.pk.startswith("Book#"), limit=10)]

    return render_template("index.html", book_data={"data":book_data})


@app.route('/get_books_categories', methods=["GET", "POST"])
def get_books_categories():
    data = json.loads(dict(request.form).get("data"))
    category = str(data.get("category"))
    print("category", category)
    data =  {"data": [x.to_json() for x in CategoriesModel.view_index.query(str(category))]}
    return data


@app.route('/get_book', methods=["GET", "POST"])
def get_book():
    data = json.loads(dict(request.form).get("data"))
    book = str(data.get("book"))
    print("book", book)
    data = {"data": [x.to_json() for x in AuthorsBooks.query(str(book))]}
    return data


if __name__ == '__main__':
    app.run(debug=True, port=5000)