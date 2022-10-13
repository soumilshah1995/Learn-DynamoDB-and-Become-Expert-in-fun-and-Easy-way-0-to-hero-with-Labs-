import json
import decimal


def dict_clean(items):
    result = {}
    for key, value in items:
        if value is None:
            value = 'n/a'
        if value == "None":
            value = 'n/a'
        if value == "null":
            value = 'n/a'
        if len(str(value)) < 1:
            value = 'n/a'
        result[key] = str(value)
    return result

import json


class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


test =  {'isbn': '1935182234', 'ttl': Decimal('1696879105'), 'gs1pk': 'Author#faaf362d-9db0-4dba-8dcf-78377e51a555', 'books_meta_data': {'longDescription': "Although several options exist for interface development in Java, even popular UI toolkits like Swing have been notoriously complex and difficult to use. Griffon, an agile framework that uses Groovy to simplify Swing, makes UI development dramatically faster and easier. In many respects, Griffon is for desktop development what Grails is for web development. While it's based on Swing, its declarative style and approachable level of abstraction is instantly familiar to developers familiar with other technologies such as Flex or JavaFX.    Griffon in Action is a comprehensive tutorial written for Java developers who want a more productive approach to UI development. In this book, you'll immediately dive into Griffon. After a Griffon orientation and a quick Groovy tutorial, you'll start building examples that explore Griffon's high productivity approach to Swing development. One of the troublesome parts of Swing development is the amount of Java code that is required to get a simple application off the ground.    You'll learn how SwingBuilder (and its cousin builders) present a very palatable alternative in the form of a DSL geared towards building graphical user interfaces. Pair it up with the convention over configuration paradigm, a well tested and tried application source structure (based on Grails) and you have a recipe for quick and effective Swing application development. Griffon in Action covers declarative view development, like the one provided by JavaFX Script, as well as the structure, architecture and life cycle of Java application development", 'shortDescription': "Griffon in Action is a comprehensive tutorial written for Java developers who want a more productive approach to UI development. In this book, you'll immediately dive into Griffon. After a Griffon orientation and a quick Groovy tutorial, you'll start building examples that explore Griffon's high productivity approach to Swing development. One of the troublesome parts of Swing development is the amount of Java code that is required to get a simple application off the ground.", 'thumbnailUrl': 'https://s3.amazonaws.com/AKIAJC5RLADLUMVRPFDQ.book-thumb-images/almiray.jpg', 'status': 'PUBLISH'}, 'author_data_object': {'AuthorName': ''}, 'book_price': '52', 'gs2pk': 'Java', 'book_title': 'Griffon in Action', 'category': 'Java', 'book_published_data': '2012-06-04T00:00:00.000-0700', 'sk': 'Book#dc6060ce-77e7-496e-a2da-52a4e07eceabAuthor#faaf362d-9db0-4dba-8dcf-78377e51a555#Category#Java', 'total_pages': '375', 'pk': 'Book#dc6060ce-77e7-496e-a2da-52a4e07eceab'}

data  = json.dumps(test, cls=CustomJsonEncoder)

new=  json.loads(data)
print(new)