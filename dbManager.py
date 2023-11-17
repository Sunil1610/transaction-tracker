from pymongo import MongoClient

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['trnsactions']
        self.splitwise = self.db['splitwise_entries']
        self.transactions = self.db['transactions']

    def insert_document(self, document, collection):
        if(self.find_document(document, collection) == None) :
            collection = self.get_collection(collection)
            return collection.insert_one(document)
        return document

    def find_document(self, query, collection):
        collection = self.get_collection(collection)
        document = collection.find_one(query)
        if(document != None) :
            document.update({"_id": str(document.get("_id"))})
        return document

    def find_documents(self, query, collection):
        collection = self.get_collection(collection)
        documents = collection.find(query)
        docs = []
        for document in documents:
            document.update({"_id": str(document.get("_id"))})
            docs.append(document)
        return docs
    
    def update_transaction(self, filter, update, collection):
        collection = self.get_collection(collection)
        return collection.update_many(filter, update)

    def delete_transaction(self, filter, collection):
        collection = self.get_collection(collection)
        return collection.delete_many(filter)

    def get_collection(self, collection) :
        if(collection == 'transactions'):
            return self.transactions
        elif(collection == 'splitwise'):
            return self.splitwise
