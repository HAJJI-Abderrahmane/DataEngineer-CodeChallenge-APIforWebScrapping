from pymongo import MongoClient


class Mongodb:
    def __init__(self):
        self.mongo_uri ="mongodb+srv://theguardianscrapper:WFEos692joKwznlu@cluster0.qgax9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.mongo_db = 'Theguardian'
        self.collection_name = 'articles'
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def close_connection(self):
        self.client.close()
    def insert_item(self, item):
        self.db[self.collection_name].insert_one(item)
    def find_item(self,query):
        doc = self.db[self.collection_name].find(query)
        return doc
