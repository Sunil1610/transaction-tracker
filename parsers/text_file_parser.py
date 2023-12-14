import csv
from datetime import datetime
from typing import List

from fastapi import HTTPException
import dbService as db

import pytz

from transactions import create_transaction_with_time
bank_names = ["paytm", "hdfc"]
def extract_transactions_from_text_file(file_content: bytes, file_name) -> list:
    text = file_content.decode('utf-8')
    transactions = []
    bank_name = None
    for bank in bank_names:
        if bank in file_name:
            bank_name = bank
            break
    reader = csv.reader(text.split("\n"), delimiter=",")
    next(reader)    
    column_definitions = None
    for row in reader:
        if(len(row) > 5) :
            if(column_definitions == None) :
                column_definitions = row
                for i in range(len(column_definitions)) :
                    column_definitions[i] = column_definitions[i].strip()
            elif(len(row) == len(column_definitions)):
                transaction = {}
                for i in range(len(row)) :
                    transaction[column_definitions[i]] = row[i].strip()
                transaction = convert_and_save_transaction(transaction, bank_name)
                transactions.append(transaction)
    return transactions

def convert_and_save_transaction(transaction: dict, bank_name: str) :
    try :
        date = transaction.get('Date')
        if(date != None) :
            date = datetime.strptime(date, '%d/%m/%y').strftime('%d/%m/%Y')
        time = None
        if(transaction.get('Date and Time') != None) :
            date, time = parse_date(transaction.get('Date and Time'))
        description = transaction.get('Narration')
        amount = transaction.get('Amount')
        sign = '-'
        if(transaction.get('Type') != None) :
            if(transaction.get('Type') == 'C') :
                sign = '+'
            if(transaction.get('Type') == 'D') :
                sign = '-'
        if(transaction.get('Debit Amount') != None and transaction.get('Debit Amount') != '0.00') :
            amount = transaction.get('Debit Amount')
            sign = '-'
        if(transaction.get('Credit Amount') != None and transaction.get('Credit Amount') != '0.00') :
            amount = transaction.get('Credit Amount')
            sign = '+'
        transaction = create_transaction_with_time(description, amount, date, sign, bank_name.upper() + "_STATEMENT", time)
        db.create_transaction(transaction, "transactions")
    except Exception as e:
        print("Error processing transaction " + str(e))
    return transaction

ist = pytz.timezone('Asia/Kolkata')
def parse_date(date_str) :
    date_object = datetime.strptime(date_str, '%d-%m-%Y %H:%M:%S')
    # Convert to IST
    date_object = date_object.replace(tzinfo=pytz.utc).astimezone(ist)

    formatted_date = date_object.strftime('%d/%m/%Y')
    formatted_time = date_object.strftime('%I:%M %p')
    return formatted_date, formatted_time