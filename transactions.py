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
    return {"Date": date, "Description": description, "Amount": amount, "Type": type, "Source": source, "timestamp": get_timestamp(date, time), "Time" : time}

def create_transaction_with_time(description, amount, date, sign, source, time):
    type = "Credit" if sign == '+' else "Debit"
    if(time == None) :
        time = "00:00:00"
    return {"Date": date, "Description": description, "Amount": amount, "Type": type, "Source": source, "Time": time, "timestamp": get_timestamp(date, time)}

def get_timestamp(date_str) :
    date_object = datetime.strptime(date_str, "%d/%m/%Y")
    return time.mktime(date_object.timetuple())

def get_timestamp(date_string, time_string):
    date_formats = ['%d/%m/%Y', '%d-%m-%Y']
    time_formats = ['%H:%M:%S', '%I:%M %p', '%I:%M:%S %p']
    for date_format in date_formats:
        try:
            date_object = datetime.strptime(date_string, date_format)
            break 
        except ValueError:
            continue 
    else:
        raise ValueError(f"No matching date format found for {date_string}")

    for time_format in time_formats:
        try:
            time_object = datetime.strptime(time_string, time_format)
            break 
        except ValueError:
            continue 
    else:
        raise ValueError(f"No matching time format found for {time_string}")
    datetime_object = datetime(
        year=date_object.year,
        month=date_object.month,
        day=date_object.day,
        hour=time_object.hour,
        minute=time_object.minute,
        second=time_object.second
    )
    return int(datetime_object.timestamp())

