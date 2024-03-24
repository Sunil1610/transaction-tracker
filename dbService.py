import subprocess
import json
import time
from typing import List
from fastapi import HTTPException
from dbManager import DatabaseManager

db_manager = DatabaseManager()

def create_transaction(transaction: dict, collection: str):
    try:
        result = db_manager.insert_document(transaction, collection)
        return result.inserted_id
    except Exception as e:
        raise HTTPException(detail=f"Error creating transaction: {str(e)}", status_code=400)

def update_transaction(query: dict, update_data: dict, collection: str):
    try:
        result = db_manager.update_transaction(query, update_data, collection)
        return {"numReplaced": result.modified_count}
    except Exception as e:
        raise HTTPException(detail=f"Error updating transaction: {str(e)}", status_code=400)

def replace_transaction(query: dict, update_data: dict, collection: str):
    try:
        result = db_manager.replace_document(query, update_data, collection)
        return {"numReplaced": result.modified_count}
    except Exception as e:
        raise HTTPException(detail=f"Error updating transaction: {str(e)}", status_code=400)

def delete_transaction(query: dict, collection: str):
    try:
        result = db_manager.delete_transaction(query, collection)
        return {"numRemoved": result.deleted_count}
    except Exception as e:
        raise HTTPException(detail=f"Error deleting transaction: {str(e)}", status_code=400)

def find_transactions(collection: str, query: dict = {}):
    try:
        result = db_manager.find_documents(query, collection)
        return result
    except Exception as e:
        raise HTTPException(detail=f"Error finding transactions: {str(e)}", status_code=400)


# def create_transaction(transaction: dict, collection: str):
#     try :
#         result = subprocess.check_output(["node", "dbOperations.js", "insert", collection, json.dumps(transaction)])
#         results_arr = result.decode().split('}\n')
#         time.sleep(0.1)
#         if(len(results_arr) > 1) :
#             result_value = results_arr[0]
#             # result_value = result_value.replace("\n", '').replace("'", '"').replace("{  ", '{ "').replace(",  ", ', "').replace(": ", '": ') + "}"
#             # return json.loads(result_value)
#             # Dummy code because too many fuck ups
#         else :
#             return results_arr[0]
#     except Exception as e:
#         raise HTTPException(detail=f"Error processing PDF: {str(e)}", status_code=400)

# def create_transactions_bulk(transactions: List[dict], collection: str):
#     try :
#         result = subprocess.check_output(["node", "dbOperations.js", "insert", collection, json.dumps(transactions)])
#         results_arr = result.decode().split('}\n')
#         if(len(results_arr) > 1) :
#             result_value = results_arr[0]
#             result_value = result_value.replace("\n", '').replace("'", '"').replace("{  ", '{ "').replace(",  ", ', "').replace(": ", '": ') + "}"
#             return json.loads(result_value)
#         else :
#             return results_arr[0]
#     except Exception as e:
#         raise HTTPException(detail=f"Error processing PDF: {str(e)}", status_code=400)

# def update_transaction(query: dict, update_data: dict, collection: str):
#     result = subprocess.check_output(["node", "dbOperations.js", "update", collection, json.dumps(query), json.dumps(update_data)])
#     return {"numReplaced": int(result)}

# def delete_transaction(query: dict, collection: str):
#     result = subprocess.check_output(["node", "dbOperations.js", "delete", collection, json.dumps(query)])
#     return {"numRemoved": int(result)}

# def find_transactions(collection: str, query: dict = {}):
#     result = subprocess.check_output(["node", "dbOperations.js", "find", collection, json.dumps(query)])
#     return json.loads(result)