def create_transaction(tran, is_credit, source):
    date = tran["Date"]
    description = tran["Description"]
    amount = tran["Amount"]
    type = "Credit" if is_credit else "Debit"
    return {"Date": date, "Description": description, "Amount": amount, "Type": type, "Source": source}
