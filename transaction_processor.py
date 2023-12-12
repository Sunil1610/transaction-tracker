
from dbManager import DatabaseManager


db_manager = DatabaseManager()

def tag_splitwise_transaction(transaction: dict) :
    amount = transaction.get('Amount')
    time = transaction.get('timestamp')
    end_time = transaction.get('timestamp') + 24 * 60 * 60
    query = {
        "timestamp" : { "$gte":time, "$lte": end_time }
    }
    docs = db_manager.find_documents(query=query, collection="splitwise")
    print(docs)
    

def tag_transactions(query: dict) :
    docs = db_manager.find_documents(query=query, collection="transactions")
    for doc in docs :
        tag_splitwise_transaction(doc)