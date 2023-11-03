import os
from fastapi import FastAPI, File, HTTPException, UploadFile
import subprocess
import json
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from pdf_extractor import extract_transactions_from_pdf
import dbService as db

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
def create_transaction(transaction: dict):
    return db.create_transaction(transaction);

@app.put("/transaction/")
def update_transaction(query: dict, update_data: dict):
    return db.update_transaction(query, update_data);

@app.delete("/transaction/")
def delete_transaction(query: dict):
    return db.delete_transaction(query)

@app.get("/transactions/")
def find_transactions(query: dict = {}):
    return db.find_transactions(query)

@app.post("/api/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    # Logic to handle and save the uploaded files...
    for file in files:
        file_content_as_bytes = await file.read()
        extract_transactions_from_pdf(file_content_as_bytes)
    return {"message": "Files uploaded successfully!"}

# Add other CRUD operations as needed...
