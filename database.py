from pymongo import MongoClient


class Mongo:
    client = MongoClient('localhost', 27017)
    db = client['test_database']

    # collection_th = db[threats.ThreatsReport.col_name]

    # create collection for samples
    @staticmethod
    def create_collection(collection_name):
        collection = Mongo.db[collection_name]
        return collection

    # add documents into collection
    @staticmethod
    def add_doc(collection, doc):
        collection_id = collection.insert_one(doc).inserted_id
        # collection_th4 = main.collection_th.insert_one(collection_id)
        # print(collection.list_collection_names())

    # collection.delete_one(post)
    # collection.delete_one(post1)
    # posts.delete_one(post)

    # for col in col_list:
    #     print(col)
    #     db.drop_collection(col)
    #     print("!!!")
    #
    # print(db.list_collection_names())

    # def insert_document(collection, data):
    #     """ Function to insert a document into a collection and return the document's id."""
    #     return collection.insert_one(data).inserted_id
    #
    # def delete_document(collection, query):
    #     """ Function to delete a single document from a collection."""
    #     collection.delete_one(query)
    #     # result = my_collection.delete_many({"name": "Mr.Geek"})

# # drop collection col1
# if col.drop():
#     print('Deleted')
# else:
#     print('Not Present')

# def find_document(collection, elements, multiple=False):
#     """ Function to retrieve single or multiple documents from a provided
#     Collection using a dictionary containing a document's elements."""
#     if multiple:
#         results = collection.find(elements)
#         return [r for r in results]
#     else:
#         return collection.find_one(elements)
