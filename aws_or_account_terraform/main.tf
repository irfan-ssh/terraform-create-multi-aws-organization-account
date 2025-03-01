#############################################
# TERRAFORM PROVIDER
#############################################
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.8.0"
    }
  }
}
provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}


#############################################
# MAIN CODE TO CRATE ORGANIZATION ACCOUNTS
#############################################

data "aws_organizations_organization" "org" {
}

# resource "aws_organizations_organization" "org" {
#   feature_set = "ALL"
# }

resource "aws_organizations_account" "aws_accounts" {
  count     = var.num_accounts
  name      = "${var.aws_account_name}${count.index + 1}"
  email     = "${var.email_name}${count.index + 1}@${var.email_domain}"
  role_name = aws_iam_role.role.name
}

#############################################
# MAIN CODE TO CRATE ORGANIZATION ACCOUNTS
#############################################
variable "account_id" {}
variable "email_name" {}
variable "email_domain" {}
variable "region" {}
variable "aws_account_name" {}
variable "access_key" {
  description = "AWS access key"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "AWS secret key"
  type        = string
  sensitive   = true
}

variable "num_accounts" {
  type = number
}
#############################################
# IAM USER ROLE AND POLICY FOR ASSUME ACCOUNT 
#############################################
resource "aws_iam_role" "role" {
  name = "Admin3rdParty"
  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Principal" : {
            "AWS" : "arn:aws:iam::${var.account_id}:root"
          },
          "Action" : "sts:AssumeRole",
          "Condition" : {}
        }
      ]
    }
  )
}

resource "aws_iam_role_policy" "policy" {
  name = "Admin-policy"
  role = aws_iam_role.role.id
  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : "*",
          "Resource" : "*"
        }
      ]
    }
  )
}



