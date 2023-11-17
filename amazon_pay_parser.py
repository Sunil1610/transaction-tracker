from datetime import datetime
import re
from typing import List
from transactions import create_transaction_with_time
import dbService as db


def extract_transactions_from_amazon(transactions: List[str]) :
    for transaction in transactions :
        form_transaction((transaction))


transaction_pattern = re.compile(
        r'(.+?(?:\n.+?)?)\n'  # Description with potential multiple lines
        r'(\d{2} \w{3} \d{4}), (\d{2}:\d{2} [APM]{2})\n'  # Date and time
        r'([+-])\s*₹([\d,]+\.*\d*)'  # Transaction sign and amount
    )

def form_transaction(transaction_str: str) :
    # Regular expression to match transaction details
    # Group 1: Description
    # Group 2: Date
    # Group 3: Time
    # Group 4: Amount sign (+/-)
    # Group 5: Amount
    
    # Find all matches in the transaction string
    try:
        matches = transaction_pattern.match(transaction_str)
        
        if not matches:
            return None
        
        # Extract details from the match
        description, date_str, time_str, sign, amount = matches.groups()
        
        description = '  '.join(description.split('\n')).strip()
        # Parse the date and time
        date_time_str = f"{date_str}, {time_str}"
        date_time = datetime.strptime(f"{date_str}, {time_str}", "%d %b %Y, %I:%M %p")
        formatted_date = date_time.strftime('%d/%m/%Y')
        transaction = create_transaction_with_time(description, amount, formatted_date, sign, "AMAZON_PAY", time_str)
        db.create_transaction(transaction, "transactions")
    except Exception as e:
        print("Error processing transaction " + str(e))

    # pattern = r'(.*?)\s+(\d{2} \w{3} \d{4}), (\d{1,2}:\d{2} [APM]{2})\s+\+\s+₹([\d,]+)'
    # match = re.search(pattern, transaction_str)
    # if match:
    #     description = match.group(1).strip()
    #     date = match.group(2).strip()
    #     time = match.group(3).strip()
    #     amount = match.group(4).strip()

    # # Print the extracted details
    #     print(f"Description: {description}")
    #     print(f"Date: {date}")
    #     print(f"Time: {time}")
    #     print(f"Amount: {amount}")
    # else:
    #     print("No transaction details could be extracted.")