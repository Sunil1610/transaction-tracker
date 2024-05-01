from datetime import datetime
import pytz
from typing import List
from transactions import create_transaction_with_time
import dbService as db


def extract_transactions_from_splitwise(transactions: List[str]):
    for transaction in transactions:
        try:
            date, time = parse_date(transaction["date"])
            tran_type, amount, tran_amount, payer = get_share(
                transaction["cost"],
                transaction["you"],
                transaction["description"]
            )
            transaction = create_transaction_with_time(
                transaction["description"],
                amount[1:],
                date,
                tran_type,
                "SPLITWISE",
                time,
            )
            transaction["Transaction_Amount"] = tran_amount[1:]
            transaction["Paid_By"] = payer.strip()
            db.create_transaction(transaction, "splitwise")
        except Exception as e:
            print("Error processing transaction " + str(e))


def get_share(cost: str, you: str, description: str):
    tran_type = "-"
    amount = "0"
    tran_amount = "0"
    payer = "you"
    cost = cost.split("\n")
    you = you.split("\n")
    if cost[0] == "you received":
        tran_type = "+"
        if len(you) == 1:
            amount = you[0]
            tran_amount = you[0]
            payer = description.split("paid")[0]
    elif "you paid" in cost[0]:
        tran_type = "+"
        if len(cost) > 1:
            tran_amount = cost[1]
        else:
            tran_amount = you[0]
        if len(you) == 1:
            amount = you[0]
        else:
            amount = you[1]
    elif "paid" in cost[0]:
        payer = cost[0].split("paid")[0]
        tran_amount = cost[1]
        if len(you) == 1:
            amount = you[0]
        else:
            amount = you[1]
    return tran_type, amount, tran_amount, payer


def parse_date(date_str):
    date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    # Convert to IST
    ist = pytz.timezone("Asia/Kolkata")
    date_object = date_object.replace(tzinfo=pytz.utc).astimezone(ist)

    formatted_date = date_object.strftime("%d/%m/%Y")
    formatted_time = date_object.strftime("%I:%M %p")
    return formatted_date, formatted_time
