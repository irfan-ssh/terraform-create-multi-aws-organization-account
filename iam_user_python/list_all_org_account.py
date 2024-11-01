import boto3

# Create an AWS Organizations client
org_client = boto3.client("organizations")

# Initialize an empty list to store all account IDs
all_account_ids = []

# Paginate through the list_accounts API to retrieve all account IDs
paginator = org_client.get_paginator('list_accounts')
for page in paginator.paginate():
    account_ids = [account["Id"] for account in page["Accounts"]]
    all_account_ids.extend(account_ids)
with open('account.txt', 'w') as f:  # Use 'w' to write a new file
    for account_id in all_account_ids:
        f.write(f'{account_id}\n')
