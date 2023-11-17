from datetime import datetime
import time

def create_transaction(tran, is_credit, source):
    date = tran["Date"]
    description = tran["Description"]
    amount = tran["Amount"].replace(",","")
    type = "Credit" if is_credit else "Debit"
    time = tran.get("Time")
    if(time == None) :
        time = "00:00:00"
    return {"Date": date, "Description": description, "Amount": amount, "Type": type, "Source": source, "timestamp": get_timestamp(date), "Time" : time}

def create_transaction_with_time(description, amount, date, sign, source, time):
    type = "Credit" if sign == '+' else "Debit"
    if(time == None) :
        time = "00:00:00"
    return {"Date": date, "Description": description, "Amount": amount, "Type": type, "Source": source, "Time": time, "timestamp": get_timestamp(date)}

def get_timestamp(date_str) :
    date_object = datetime.strptime(date_str, "%d/%m/%Y")
    return time.mktime(date_object.timetuple())
