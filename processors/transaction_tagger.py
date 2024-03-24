import dbService as db
from bson import ObjectId

def tag_corresponding_splitwise_entry(transaction) :
    # 2 days from transaction is the cushion
    timeCushion = 2*24*60*60
    splitwise_entries = db.find_transactions( "splitwise", {
        "timestamp":{"$gt": transaction.timestamp, "$lt": transaction.timestamp + timeCushion}
    })


def parse_transactions_to_number():
    for tran in db.find_transactions("splitwise", {}) :
        id = tran['_id']
        del tran['_id']
        tran['Transaction_Amount'] = float(tran['Transaction_Amount'])
        tran['Amount'] = float(tran['Amount'])
        db.replace_transaction({"_id":ObjectId(id)}, tran, "splitwise")