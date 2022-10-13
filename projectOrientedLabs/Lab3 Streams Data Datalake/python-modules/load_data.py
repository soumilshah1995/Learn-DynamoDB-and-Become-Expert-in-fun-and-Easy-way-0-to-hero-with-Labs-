try:
    from faker import Faker
    import uuid
    import datetime
    import  json
    import random
    from dateutil.relativedelta import relativedelta
    from datetime import datetime

    from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
    from pynamodb.models import Model
    from pynamodb.attributes import *
    from dotenv import load_dotenv
    import os


    load_dotenv("../.env")
    from data import BOOKS_DATA

except Exception as e:pass


global TABLE_NAME
TABLE_NAME = f'{os.getenv("TABLE_NAME")}-lab-{os.getenv("LAB_NUMBER")}-team-{os.getenv("TEAM_NUMBER")}'
print(TABLE_NAME, "**")

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


def clean_table():
    for x in AuthorsBooks.scan():
        x.delete()

def get_current_timestamp():
    # current date and time
    ttl_time = datetime.now() + relativedelta(years=2)
    timestamp = datetime.timestamp(datetime.now() + relativedelta(years=1))
    return round(timestamp)


def load_data_sets():
    clean_table()
    for c, items in enumerate(BOOKS_DATA):
        try:
            print(c)
            for author in items.get("authors"):

                author_id = uuid.uuid4().__str__()

                AuthorsBooks(
                    pk=f"Author#{author_id}",
                    sk=f"Author#{author_id}",
                    author_data_object={
                        "AuthorName":author
                    },
                    ttl=get_current_timestamp()
                ).save()

                book_id = uuid.uuid4().__str__()

                if items.get("categories") == []:
                    res = AuthorsBooks(
                        pk=f"Book#{book_id}",
                        sk=f"Book#{book_id}#Author#{author_id}",
                        book_title=items.get("title"),
                        book_published_data=items.get("publishedDate", {}).get("$date"),
                        book_price = random.randint(20,300).__str__(),
                        isbn=items.get("isbn").__str__(),
                        total_pages=items.get("pageCount").__str__(),
                        author_data_object={
                            "AuthorName":author

                        },
                        books_meta_data={
                            "thumbnailUrl":items.get("thumbnailUrl"),
                            "shortDescription":items.get("shortDescription"),
                            "longDescription":items.get("longDescription"),
                            "status":items.get("status"),
                        },
                        category="",
                        gs1pk=f"Author#{author_id}",
                        gs2pk="",
                        ttl=get_current_timestamp()
                    ).save()

                else:
                    for category in items.get("categories"):
                        res = AuthorsBooks(
                            pk=f"Book#{book_id}",
                            sk=f"Book#{book_id}Author#{author_id}#Category#{category}",
                            book_title=items.get("title"),
                            book_published_data=items.get("publishedDate", {}).get("$date"),
                            book_price = random.randint(20,300).__str__(),
                            isbn=items.get("isbn").__str__(),
                            total_pages=items.get("pageCount").__str__(),
                            author_data_object={
                                "AuthorName":author

                            },
                            books_meta_data={
                                "thumbnailUrl":items.get("thumbnailUrl"),
                                "shortDescription":items.get("shortDescription"),
                                "longDescription":items.get("longDescription"),
                                "status":items.get("status"),
                            },
                            category=category,
                            gs1pk=f"Author#{author_id}",
                            gs2pk = category,
                            ttl=get_current_timestamp()
                        ).save()
        except Exception as e:
            pass


def  get_categories():

    for cat in CategoriesModel.view_index.scan():

        try:
            AuthorsBooks(
                pk=f"categoryList#",
                sk=str(cat.category)
            ).save()
        except Exception as e:
            pass



if __name__ == '__main__':
    load_data_sets()
    get_categories()