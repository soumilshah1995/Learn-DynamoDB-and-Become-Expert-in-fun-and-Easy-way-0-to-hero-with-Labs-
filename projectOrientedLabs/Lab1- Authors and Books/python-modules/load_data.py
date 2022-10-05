
try:
    from faker import Faker
    import uuid
    import datetime
    import  json
    import random
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    from helper import AuthorsBooks
except Exception as e:pass


def generate_authors(alias_name='author_'):
    faker = Faker()
    _ = faker.simple_profile()
    _['{}id'.format(alias_name)] = uuid.uuid4().__str__()
    _['birthdate'] = _.pop("birthdate").__str__()
    return _


def generate_books(alias_name='book_'):

    faker = Faker()
    _= {}
    _['{}id'.format(alias_name)] = uuid.uuid4().__str__()
    _["book_title"] = faker.text()
    _['book_published_data'] = faker.date()
    _['book_price'] = random.randint(30,200)

    _['isbn'] = random.randint(30200, 200231)
    _['total_pages'] = random.randint(100, 2000)

    return _

def clean_table():
    for x in AuthorsBooks.scan():
        x.delete()


def get_current_timestamp():
    # current date and time
    ttl_time = datetime.now() + relativedelta(years=2)
    timestamp = datetime.timestamp(datetime.now() + relativedelta(years=2))
    return round(timestamp)


def main():

    clean_table()
    total_users = 3
    total_books = 5
    total_category_book_can_have = 2

    book_categories = ["Fantasy", "SciFi", "AWS", "Cloud Computing","horror"]

    for i in range(0, total_users):
        json_data = generate_authors()
        AuthorsBooks(
            pk=f"Author#{json_data.get('author_id')}",
            sk=f"Author#{json_data.get('author_id')}",
            author_data_object= json_data
        ).save()

    Author = [Author for Author in AuthorsBooks.scan(AuthorsBooks.pk.startswith("Author#"))]

    for book in range(0, total_books):
        book_data = generate_books()
        total_author_who_worked_on_this_book = random.randint(0, len(Author) - 1)

        for author in range(total_author_who_worked_on_this_book):

            book_data = book_data
            author_data = random.choice(Author)

            for category in random.sample(book_categories, total_category_book_can_have):
                res = AuthorsBooks(
                    pk=f"Book#{book_data.get('book_id')}",
                    sk=f"Book#{book_data.get('book_id')}#{author_data.pk}#Category#{category}",
                    book_title=book_data.get("book_title"),
                    book_published_data=book_data.get("book_published_data").__str__(),
                    book_price=book_data.get("book_price").__str__(),
                    isbn=book_data.get("isbn").__str__(),
                    total_pages=book_data.get("total_pages").__str__(),
                    author_data_object=json.loads(author_data.to_json()),
                    category=category,
                    gs1pk=f"{author_data.pk}",
                    gs2pk = f"{category}",
                ).save()


    for category in book_categories:
        AuthorsBooks(
            pk='CategoryList',
            sk=category
        ).save()


if __name__ == '__main__':
    main()