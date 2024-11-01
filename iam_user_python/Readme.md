# AWS IAM User Creation Script

This Python script uses the Boto3 library to create IAM users in multiple AWS accounts. The script assumes a role in each specified account, creates a user with Administrator access, and saves the access keys to a file.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage Instructions](#usage-instructions)
- [Important Notes](#important-notes)
- [Script Overview](#script-overview)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.x installed on your machine.
- Boto3 library installed. You can install it using pip:

  ```bash
  pip install boto3
