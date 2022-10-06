
try:
    from faker import Faker
    import uuid
    import datetime
    import  json
    import random
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    from helper import AuthorsBooks
    from data import BOOKS_DATA
except Exception as e:pass


def generate_authors(item):
    faker = Faker()

    for author in item.get("authors"):

        _ = {}
        _['author_id'] = uuid.uuid4().__str__()
        _["author_name"] = item.get("")

    return _


def generate_books(alias_name='book_'):

    faker = Faker()
    _= {}
    _['{}id'.format(alias_name)] = uuid.uuid4().__str__()
    book =  random.choice(books_dataset.get("books"))
    _["book_title"] =book.get("title")
    _['book_published_data'] = book.get("published").__str__()
    _['book_price'] = random.randint(30, 200).__str__()
    _['isbn'] = book.get("isbn").__str__()
    _['total_pages'] = book.get("pages").__str__()

    return _

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
                        sk=f"Book#{book_id}#{author_id}",
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
                        gs1pk=author_id,
                        gs2pk = "",
                        ttl=get_current_timestamp()
                    ).save()
                else:
                    for category in items.get("categories"):
                        res = AuthorsBooks(
                            pk=f"Book#{book_id}",
                            sk=f"Book#{book_id}#{author_id}#Category#{category}",
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
                            gs1pk=author_id,
                            gs2pk = category,
                            ttl=get_current_timestamp()
                        ).save()
        except Exception as e:
            pass

if __name__ == '__main__':
    load_data_sets()