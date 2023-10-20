import os
from fastapi import FastAPI, File, HTTPException, UploadFile
import subprocess
import json

from fastapi.staticfiles import StaticFiles

from pdf_extractor import extract_transactions_from_pdf

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui"), name="ui")

@app.post("/transaction/")
def create_transaction(transaction: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "insert", json.dumps(transaction)])
    return json.loads(result)

@app.put("/transaction/")
def update_transaction(query: dict, update_data: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "update", json.dumps(query), json.dumps(update_data)])
    return {"numReplaced": int(result)}

@app.delete("/transaction/")
def delete_transaction(query: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "delete", json.dumps(query)])
    return {"numRemoved": int(result)}

@app.delete("/transaction/")
def delete_transaction(query: dict):
    result = subprocess.check_output(["node", "dbOperations.js", "delete", json.dumps(query)])
    return {"numRemoved": int(result)}

@app.get("/transactions/")
def find_transactions(query: dict = {}):
    result = subprocess.check_output(["node", "dbOperations.js", "find", json.dumps(query)])
    return json.loads(result)

@app.post("/api/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    # Logic to handle and save the uploaded files...
    for file in files:
        file_content_as_bytes = await file.read()
        extract_transactions_from_pdf(file_content_as_bytes)
    return {"message": "Files uploaded successfully!"}

# Add other CRUD operations as needed...
