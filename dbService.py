import subprocess
import json


def create_transaction(transaction: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "insert", json.dumps(transaction)])
    return json.loads((result.decode().split('}\n')[1] + "}"))

def update_transaction(query: dict, update_data: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "update", json.dumps(query), json.dumps(update_data)])
    return {"numReplaced": int(result)}

def delete_transaction(query: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "delete", json.dumps(query)])
    return {"numRemoved": int(result)}

def find_transactions(query: dict = {}):
    result = subprocess.check_output(["node", "dbOperations.js", "find", json.dumps(query)])
    return json.loads(result)