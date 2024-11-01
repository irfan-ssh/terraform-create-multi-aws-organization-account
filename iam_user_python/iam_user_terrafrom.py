import boto3

account_file = input("Please enter Account id file path ::  ")
# Read account IDs from account.txt
with open(account_file, 'r') as f:
    account_ids = [line.strip() for line in f]

for account_id in account_ids:
    # Assume a role in the AWS account
    sts_client = boto3.client("sts")
    assumed_role = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/Admin",
        RoleSessionName="AssumedRoleSession",
    )

    # Create a Boto3 client using the assumed role's credentials
    try:
        iam = boto3.client(
            "iam",
            aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role["Credentials"]["SecretAccessKey"],
            aws_session_token=assumed_role["Credentials"]["SessionToken"],
        )
        
        policy = 'arn:aws:iam::aws:policy/AdministratorAccess'
        user_name = f'User-{account_id}'  # Generate a unique user name for each account
        
        response = iam.create_user(UserName=user_name)
        
        add_policy = iam.attach_user_policy(
            PolicyArn=policy,
            UserName=user_name,
        )

        create_key = iam.create_access_key(UserName=user_name)
        access_key = create_key["AccessKey"]["AccessKeyId"]
        secret_key = create_key["AccessKey"]["SecretAccessKey"]

        with open('data.txt', 'a') as f:  # Use 'a' to append to the file
            f.write(f'{access_key}:{secret_key}\n')

        print(f'User updated in Account ID: {account_id} and written to data.txt file')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
