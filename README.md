# Terraform AWS Organization Accounts Setup

This Terraform configuration sets up AWS Organization accounts and an IAM role with policies to assume those accounts. It allows you to create multiple AWS accounts under an organization and assign an administrative role for account management.

## Prerequisites

- Terraform installed (version 1.0 or higher recommended)
- AWS CLI installed and configured with the necessary permissions
- An AWS account with permissions to create organizations and accounts

## Configuration

Before running the Terraform configuration, you need to define the following variables in the `terraform.tfvars` file:

### Variables

- `account_id`: The AWS account ID that will be allowed to assume the IAM role.  
- `region`: The AWS region where the resources will be created (e.g., `us-east-1`).
- `email_name`: The base name for the email addresses of the new accounts.
- `email_domain`: The domain for the email addresses of the new accounts (e.g., `gmail.com`).
- `aws_account_name`: The base name for the AWS accounts to be created.
- `num_accounts`: The number of AWS accounts to create.

### Example `terraform.tfvars`

```hcl
account_id       = "xxxxxxxxxxxx"
region           = "us-east-1"
email_name       = "AlbertAWS0"
email_domain     = "gmail.com"
aws_account_name = "AWS"
num_accounts     = 620
