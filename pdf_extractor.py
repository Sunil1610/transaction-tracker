import io
import re
from fastapi import HTTPException
import PyPDF2

from transactions import create_transaction

def extract_transactions_from_pdf(file_content: bytes) -> str:
    text_content = ""
    try:
        # Use BytesIO to read the byte content as a file
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))

        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()
        type = get_source(text_content)
        if(type != "") :
            delimiters = get_delimiters(type)
            if(delimiters != "") :
                pattern = "|".join(map(re.escape, delimiters))
                parts = re.split(pattern, text_content)
                transactionList = ''
                for part_num in range(len(parts)):
                    tran_str = parts[part_num].lstrip()
                    pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}"
                    if(bool(re.match(pattern, tran_str))) :
                        transactionList+= "\n" + tran_str
                parse_and_save(transactionList)
    except Exception as e:
        raise HTTPException(detail=f"Error processing PDF: {str(e)}", status_code=400)
    return text_content

def parse_and_save(tran_str) :
    transactions = tran_str.split("\n")
    entries = []
    for line in transactions:
        line = remove_leading_special_chars(line.strip())
        is_credit_transaction = line.endswith(" Cr")
        if is_credit_transaction:
            line = line[:-3]
        transaction = parse_transaction(line, is_credit_transaction)
        if transaction:
            entries.append(transaction)
    print(entries)        

def remove_leading_special_chars(s):
    return re.sub(r"^[^A-Za-z0-9]+", "", s)

def get_source(text) :
    if("Diners Club International Credit Card" in text) : return "DINERS";
    if("SWIGGY ORANGE CARD" in text) : return "SWIGGY";
    
    return "";

def get_delimiters(type) :
    if(type == "DINERS") : return ["ANGARA SUNIL", "Reward Points Summary", "Diners Club"]
    if(type == "SWIGGY") : return ["ANGARA CHANDRA", "Reward Points Summary", "SWIGGY ORANGE CARD", "Swiggy Cashback Summary"]
    
    return "";

def parse_transaction(line, is_credit_transaction):
    patterns = [
        (r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) ([A-Z0-9a-z\s.]+) ([A-Z0-9a-z\s.]+) (\d+\.?\d{0,2})',
         lambda groups: {"Date": groups[0], "Time": groups[1], "Description": f"{groups[2].strip()} {groups[3].strip()}", "Amount": groups[4]}),
        
        (r'(\d+) (\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) ([A-Z0-9a-z\s.]+) ([A-Z0-9a-z\s.]+) (\d+\.?\d{0,2})',
         lambda groups: {"Date": groups[1], "Time": groups[2], "Description": f"{groups[3].strip()} {groups[4].strip()}", "Amount": groups[5]}),
        
        (r'(\d{2}/\d{2}/\d{4}) ([A-Za-z0-9\s.]+) (\d+\.?\d{0,2})',
         lambda groups: {"Date": groups[0], "Description": groups[1].strip(), "Amount": groups[2]}),
        
        (r'(\d+) (\d{2}/\d{2}/\d{4}) ([A-Za-z0-9\s.]+) (\d+\.?\d{0,2})',
         lambda groups: {"Date": groups[1], "Description": groups[2].strip(), "Amount": groups[3], "Type": "Credit"})
    ]

    for pattern, mapper in patterns:
        match = re.match(pattern, line)
        if match:
            transaction = mapper(match.groups())
            transaction = create_transaction(transaction, is_credit_transaction)
            return transaction
    return None

