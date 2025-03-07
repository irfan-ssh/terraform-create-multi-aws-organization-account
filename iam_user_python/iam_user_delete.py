import boto3
import time
import botocore.exceptions

account_file = input("Please enter Account id file path ::  ")

# Read account IDs from the specified file
with open(account_file, 'r') as f:
    account_ids = [line.strip() for line in f]

success_count = 0
error_count = 0
skipped_count = 0

for account_id in account_ids:
    # Assume a role in the AWS account
    try:
        print(f"Processing Account ID: {account_id}")
        sts_client = boto3.client("sts")
        
        try:
            assumed_role = sts_client.assume_role(
                RoleArn=f"arn:aws:iam::{account_id}:role/Admin3rdParty",
                RoleSessionName="AssumedRoleSession",
            )
        except botocore.exceptions.ClientError as e:
            print(f"Error assuming role in Account ID: {account_id}: {str(e)}")
            error_count += 1
            continue  # Skip to the next account

        # Create a Boto3 client using the assumed role's credentials
        iam = boto3.client(
            "iam",
            aws_access_key_id=assumed_role["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role["Credentials"]["SecretAccessKey"],
            aws_session_token=assumed_role["Credentials"]["SessionToken"],
        )
        
        user_name = f'User-{account_id}'  # Generate the user name based on account ID
        
        try:
            # First, list all access keys for the user
            try:
                access_keys = iam.list_access_keys(UserName=user_name)
                
                # Delete all access keys for the user
                for key in access_keys.get('AccessKeyMetadata', []):
                    access_key_id = key['AccessKeyId']
                    # print(f"Deleting access key {access_key_id} for user {user_name}")
                    iam.delete_access_key(
                        UserName=user_name,
                        AccessKeyId=access_key_id
                    )
                
                # List all attached policies for the user
                attached_policies = iam.list_attached_user_policies(UserName=user_name)
                
                # Detach all policies from the user
                for policy in attached_policies.get('AttachedPolicies', []):
                    policy_arn = policy['PolicyArn']
                    # print(f"Detaching policy {policy_arn} from user {user_name}")
                    iam.detach_user_policy(
                        UserName=user_name,
                        PolicyArn=policy_arn
                    )
                
                # Finally, delete the user
                iam.delete_user(UserName=user_name)
                print(f"Successfully deleted user {user_name} from Account ID: {account_id}")
                success_count += 1
                
            except iam.exceptions.NoSuchEntityException:
                print(f"User {user_name} not found in Account ID: {account_id}")
                skipped_count += 1
                
            # Add a small delay to avoid hitting API rate limits
            time.sleep(1)
            
        except Exception as e:
            print(f"Error deleting user {user_name} in Account ID: {account_id}: {str(e)}")
            error_count += 1
            
    except Exception as e:
        print(f"Unexpected error with Account ID: {account_id}: {str(e)}")
        error_count += 1

print("\n----- Summary -----")
print(f"Total accounts processed: {len(account_ids)}")
print(f"Successful deletions: {success_count}")
print(f"Users not found (skipped): {skipped_count}")
print(f"Errors encountered: {error_count}")
print("User deletion process completed.")