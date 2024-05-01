from dbManager import DatabaseManager
import dbService as db


db_manager = DatabaseManager()


def tag_splitwise_transaction(transaction: dict):
    # amount = transaction.get("Amount")
    time = transaction.get("timestamp")
    end_time = transaction.get("timestamp") + 24 * 60 * 60
    query = {"timestamp": {"$gte": time, "$lte": end_time}}
    docs = db_manager.find_documents(query=query, collection="splitwise")
    print(docs)


def tag_transactions(query: dict):
    docs = db_manager.find_documents(query=query, collection="transactions")
    for doc in docs:
        tag_splitwise_transaction(doc)


def insert_splitwise_expenses():
    splitwise_transactions = db_manager.find_documents(
        query={}, collection="splitwise"
    )
    for splitwise_transaction in splitwise_transactions:
        if splitwise_transaction["Type"] == "Debit":
            new_transaction = splitwise_transaction
            new_transaction["splitwise_id"] = new_transaction["_id"]
            del new_transaction["_id"]
            db.create_transaction(splitwise_transaction, "transactions")
