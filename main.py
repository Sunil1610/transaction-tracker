import os
from typing import List
from fastapi import FastAPI, File, HTTPException, UploadFile
import subprocess
import json
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from parsers.amazon_pay_parser import extract_transactions_from_amazon
from parsers.splitwise_parser import extract_transactions_from_splitwise
from parsers.pdf_extractor import extract_transactions_from_pdf
from parsers.pdf_extractor_json import readEmails
import dbService as db
from parsers.text_file_parser import extract_transactions_from_text_file
from processors.transaction_tagger import parse_transactions_to_number
from transaction_processor import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/upload", StaticFiles(directory="ui"), name="upload")
react_build_folder = Path(__file__).parent / "finance-app" / "build"


@app.get("/ui/{path:path}")
def serve_root(path: str):
    file_path = react_build_folder / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(react_build_folder / "index.html")


@app.post("/transaction/")
def create_transaction(transaction: dict, collection:str = "transactions"):
    return db.create_transaction(transaction, collection)


@app.put("/transaction/")
def update_transaction(query: dict, update_data: dict, collection: str = "transactions"):
    return db.update_transaction(query, update_data, collection)


@app.delete("/transaction/")
def delete_transaction(query: dict, collection: str = "transactions"):
    return db.delete_transaction(query, collection)


@app.get("/transactions/")
def find_transactions(query: dict = {}, collection: str = "transactions"):
    return db.find_transactions(collection, query)



@app.post("/api/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    # Logic to handle and save the uploaded files...
    for file in files:
        file_content_as_bytes = await file.read()
        content_type = file.content_type
        if "pdf" in content_type:
            extract_transactions_from_pdf(file_content_as_bytes, file.filename)
        elif "text" in content_type:
            extract_transactions_from_text_file(file_content_as_bytes, file.filename)
    return {"message": "Files uploaded successfully!"}

@app.post("/mail/get/")
async def upload_files(extractor: str, limit: int):
    # Logic to handle and save the uploaded files...
    readEmails(extractor, limit)
    return {"message": "Files uploaded successfully!"}


@app.post("/api/upload/amazon_pay")
async def upload_amazon_tran(amazon_transactions: List[dict]):
    extract_transactions_from_amazon(amazon_transactions)


@app.post("/api/process/transactions")
async def process_tran():
    parse_transactions_to_number()


@app.post("/api/upload/splitwise")
async def upoad_splitwise_tran(splitwise_transactions: List[dict]):
    extract_transactions_from_splitwise(splitwise_transactions)

@app.post("/api/process/splitwise")
async def process_splitwise_expenses():
    insert_splitwise_expenses()


@app.post("/api/tag/splitwise")
async def tag_transactions(query: dict = {}):
    # Logic to handle and save the uploaded files...
    tag_transactions(query)


# Add other CRUD operations as needed...
