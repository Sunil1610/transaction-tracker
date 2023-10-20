import io
import re
from fastapi import HTTPException
import PyPDF2

def extract_transactions_from_pdf(file_content: bytes) -> str:
    text_content = ""
    try:
        # Use BytesIO to read the byte content as a file
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))

        # Loop through each page and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text()
        delimiters = ["ANGARA SUNIL", "Reward Points Summary", "Diners Club"]
        pattern = "|".join(map(re.escape, delimiters))
        parts = re.split(pattern, text_content)
        transactionList = ''
        for part_num in range(len(parts)):
            tran_str = parts[part_num].lstrip()
            pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}"
            if(bool(re.match(pattern, tran_str))) :
                transactionList+= tran_str
        parse_and_save(transactionList)
    except Exception as e:
        raise HTTPException(detail=f"Error processing PDF: {str(e)}", status_code=400)
    return text_content

def parse_and_save(tran_str) :
    transactions = tran_str.split("\n")
    entries = []
    for line in transactions :
        line = remove_leading_special_chars(line.lstrip())
        match1 = re.match(r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) ([A-Z0-9a-z\s.]+) ([A-Z0-9a-z\s.]+) (\d+\.?\d{0,2})', line)
        match2 = re.match(r'(\d+) (\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}:\d{2}) ([A-Z0-9a-z\s.]+) ([A-Z0-9a-z\s.]+) (\d+\.?\d{0,2})', line)
        match3 = re.match(r'(\d{2}/\d{2}/\d{4}) ([A-Za-z0-9\s.]+) (\d+\.?\d{0,2}) Cr', line)
        match4 = re.match(r'(\d+) (\d{2}/\d{2}/\d{4}) ([A-Za-z0-9\s.]+) (\d+\.?\d{0,2}) Cr', line)
        if match3:
            date, company, amount = match3.groups()
            entries.append({"Date": date, "Company": company.strip(), "Amount": amount, "Type": "Credit"})
        elif match4:
            id_num, date, company, amount = match4.groups()
            entries.append({"Date": date, "Company": company.strip(), "Amount": amount, "Type": "Credit"})
        elif match1:
            date, time, company, location, amount = match1.groups()
            entries.append({"Date": date, "Time": time, "Company": company.strip(), "Amount": amount, "Type": "Debit"})
        elif match2:
            id_num, date, time, company, location, amount = match2.groups()
            entries.append({"Date": date, "Time": time, "Company": company.strip(), "Amount": amount, "Type": "Debit"})
    print(entries)        

def remove_leading_special_chars(s):
    return re.sub(r"^[^A-Za-z0-9]+", "", s)