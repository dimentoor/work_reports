# connection to database soon
import threats
import pymongo
import pandas as pd
from pymongo import MongoClient


class Mongo:
    def __init__(self):
        pass


def mongo_test():
    client = MongoClient('localhost', 27017)
    # database
    db = client['work_reports']

    # collection
    # collection = db['test1_collection']
    # posts = db['posts']
    threats = db['threats_col']

# convert df to json
    df.to_json(orient="columns")

    принимаем коллекецию
    записываем ее базу данных
    работа с базой данных
    # collection_id = collection.insert_one(post)
    # collection_id = collection.insert_one(post1)
    # post_id = posts.insert_one(post).inserted_id

    col_list = db.list_collection_names()
    print(db.list_collection_names())
    # post = {"author": "Mike",
    #         "text": "My first blog post!",
    #         "tags": ["mongodb", "python", "pymongo"],
    #         "date": '55'}
    # post1 = {"author": "777",
    #          "text": "8888",
    #          "tags": ["89", "python", "pymongo"],
    #          "date": '00'}
    # collection.delete_one(post)
    # collection.delete_one(post1)
    # posts.delete_one(post)

    # for col in col_list:
    #     print(col)
    #     db.drop_collection(col)
    #     print("!!!")
    #
    # print(db.list_collection_names())


def insert_document(collection, data):
    """ Function to insert a document into a collection and return the document's id."""
    return collection.insert_one(data).inserted_id


def delete_document(collection, query):
    """ Function to delete a single document from a collection."""
    collection.delete_one(query)
    # result = my_collection.delete_many({"name": "Mr.Geek"})


# # drop collection col1
# if col.drop():
#     print('Deleted')
# else:
#     print('Not Present')

def find_document(collection, elements, multiple=False):
    """ Function to retrieve single or multiple documents from a provided
    Collection using a dictionary containing a document's elements."""
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)
