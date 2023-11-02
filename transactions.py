def create_transaction(tran, is_credit):
    date = tran["Date"]
    description = tran["Description"]
    amount = tran["Amount"]
    type = "Credit" if is_credit else "Debit"
    return {"Date": date, "Description": description, "Amount": amount, "Type": type}
