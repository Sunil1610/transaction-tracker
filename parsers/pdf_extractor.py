import io
import re
import PyPDF2
import dbService as db
from transactions import create_transaction
from utils import remove_leading_special_chars
import logging


def extract_transactions_from_protected_pdf(file_content, passwords: [str]) -> str:
    text_content = ""
    for password in passwords:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content), password=password)
            if pdf_reader.is_encrypted:
                pdf_reader.decrypt(password)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text()
            parse_pdf_content(text_content, '')
        except Exception as err:
            logging.error(f"An error occurred: {err}")
    return text_content


def extract_transactions_from_pdf(file_content: bytes, file_name: str) -> str:
    text_content = ""
    try:
        # Use BytesIO to read the byte content as a file
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))

        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()
        parse_pdf_content(text_content, file_name)
    except Exception as e:
        print("Error processing transaction " + str(e))
    return text_content


def parse_pdf_content(text_content: str, file_name: str):
    source = get_source(text_content, file_name)
    transactions = []
    if source != "":
        delimiters = get_delimiters(source)
        if delimiters != "":
            pattern = "|".join(map(re.escape, delimiters))
            parts = re.split(pattern, text_content)
            transaction_list = ''
            for part_num in range(len(parts)):
                tran_str = parts[part_num].lstrip()
                pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}"
                if bool(re.match(pattern, tran_str)):
                    transaction_list += "\n" + tran_str
            transactions = parse(transaction_list, source)
    for transaction in transactions:
        db.create_transaction(transaction, "transactions")


def parse(tran_str, source):
    transactions = tran_str.split("\n")
    entries = []
    for line in transactions:
        line = remove_leading_special_chars(line.strip())
        is_credit_transaction = line.endswith(" Cr")
        if is_credit_transaction:
            line = line[:-3]
        transaction = parse_transaction(line, is_credit_transaction, source)
        if transaction:
            entries.append(transaction)
    return entries


def get_source(text, filename: str):
    if "Diners Club International Credit Card" in text:
        return "DINERS_CRED_CARD"
    if "SWIGGY ORANGE CARD" in text:
        return "SWIGGY_CRED_CARD"
    if filename.lower().startswith("swiggy"):
        return "SWIGGY_CRED_CARD"
    return ""


def get_delimiters(type):
    if type == "DINERS_CRED_CARD":
        return ["ANGARA SUNIL", "Reward Points Summary", "Diners Club"]
    if type == "SWIGGY_CRED_CARD":
        return ["ANGARA CHANDRA", "Reward Points Summary", "SWIGGY ORANGE CARD", "Swiggy Cashback Summary"]

    return ""


def parse_transaction(line, is_credit_transaction, source):
    patterns = [
        (r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) ([A-Z0-9a-z\s.]+) ([A-Z0-9a-z\s.]+) ((\d*,\d*)*\d+\.?\d{0,4})',
         lambda groups: {"Date": groups[0], "Time": groups[1], "Description": f"{groups[2].strip()}",
                         "Amount": groups[4]}),

        (r'(\d+) (\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) ([A-Z0-9a-z\s.]+) ([A-Z0-9a-z\s.]+) ((\d*,\d*)*\d+\.?\d{0,4})',
         lambda groups: {"Date": groups[1], "Time": groups[2], "Description": f"{groups[3].strip()}",
                         "Amount": groups[5]}),

        (r'(\d{2}/\d{2}/\d{4}) ([A-Za-z0-9\s.]+) ((\d*,\d*)*\d+\.?\d{0,4})',
         lambda groups: {"Date": groups[0], "Description": groups[1].strip(), "Amount": groups[2]}),

        (r'(\d+) (\d{2}/\d{2}/\d{4}) ([A-Za-z0-9\s.]+) ((\d*,\d*)*\d+\.?\d{0,4})',
         lambda groups: {"Date": groups[1], "Description": groups[2].strip(), "Amount": groups[3], "Type": "Credit"})
    ]

    for pattern, mapper in patterns:
        match = re.match(pattern, line)
        if match:
            transaction = mapper(match.groups())
            transaction = create_transaction(transaction, is_credit_transaction, source)
            return transaction
    return None
