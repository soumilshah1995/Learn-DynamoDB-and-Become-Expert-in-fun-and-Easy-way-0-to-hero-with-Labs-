try:
    from flask import Flask, render_template
    import uuid
    import os
    import json

    import boto3
    from datetime import datetime
    from flask import request

    from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
    from dotenv import load_dotenv
    from helper import (get_sample_books,
                        get_books_categories_from_dynamo_db,
                        get_book_from_dynamodb,
                        get_categories_auto_complete)

    load_dotenv("../.env")

except Exception as e:
    print("Error", e)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    json_data = get_sample_books()
    return render_template("index.html", book_data=json_data)


@app.route("/get_books_categories", methods=["GET", "POST"])
def get_books_categories():
    request_data = dict(request.form)
    param = json.loads(request_data.get("data"))
    print("""param.get("category")""", param.get("category"))
    data = get_books_categories_from_dynamo_db(param.get("category"))
    return data


@app.route("/get_book", methods=["GET", "POST"])
def get_book():
    data = json.loads(dict(request.form).get("data"))
    book = data.get("book")
    json_data = get_book_from_dynamodb(book=book)
    return json_data


@app.route("/get_all_category", methods=["GET", "POST"])
def get_all_category():
    data = get_categories_auto_complete()
    return {"data":data}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
