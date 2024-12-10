import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Function to fetch transaction data from a public API
def fetch_transactions(api_url):
    """
    Fetch transaction data from a public API.
    Replace with a real API endpoint for production.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Fraud detection function
def detect_fraud(transactions, amount_threshold=10000, time_window_minutes=60, frequency_limit=5):
    """
    Detects suspicious transactions based on thresholds.

    :param transactions: List of transaction dictionaries.
    :param amount_threshold: Maximum allowable transaction amount.
    :param time_window_minutes: Time window to analyze frequency of transactions.
    :param frequency_limit: Max allowable transactions per account within the time window.
    :return: List of flagged transactions and reason for flagging.
    """
    flagged_transactions = []
    account_activity = defaultdict(list)

    # Convert timestamps to datetime objects for analysis
    for txn in transactions:
        txn['timestamp'] = datetime.strptime(txn['timestamp'], '%Y-%m-%d %H:%M:%S')

    # Check each transaction
    for txn in transactions:
        account_id = txn['account_id']
        amount = txn['amount']
        timestamp = txn['timestamp']

        # Rule 1: Check if the transaction amount exceeds the threshold
        if amount > amount_threshold:
            flagged_transactions.append({
                "transaction": txn,
                "reason": f"Amount exceeds threshold of {amount_threshold}"
            })

        # Rule 2: Check for frequency of transactions within the time window
        account_activity[account_id].append(timestamp)
        recent_transactions = [t for t in account_activity[account_id] if t > timestamp - timedelta(minutes=time_window_minutes)]

        if len(recent_transactions) > frequency_limit:
            flagged_transactions.append({
                "transaction": txn,
                "reason": f"More than {frequency_limit} transactions within {time_window_minutes} minutes"
            })

    return flagged_transactions

# Main execution
def main():
    # Mock API URL (replace with a real endpoint)
    api_url = "https://api.example.com/transactions"

    print("Fetching transactions from API...")
    transactions = fetch_transactions(api_url)

    if not transactions:
        print("No transactions fetched. Exiting.")
        return

    print(f"Fetched {len(transactions)} transactions. Analyzing for fraud...")
    flagged_transactions = detect_fraud(transactions)

    if flagged_transactions:
        print(f"Suspicious transactions detected: {len(flagged_transactions)}")
        for idx, flag in enumerate(flagged_transactions, 1):
            txn = flag["transaction"]
            print(f"\nSuspicious Transaction {idx}:")
            print(f"Account ID: {txn['account_id']}")
            print(f"Amount: {txn['amount']}")
            print(f"Timestamp: {txn['timestamp']}")
            print(f"Reason: {flag['reason']}")
    else:
        print("No suspicious transactions detected.")

# Example usage
if __name__ == "__main__":
    main()
