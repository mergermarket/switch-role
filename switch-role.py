import sys
import argparse
import boto3
import re

parser = argparse.ArgumentParser(
    description='Switch to IAM role on the command-line'
)
parser.add_argument(
    '--role-arn', help='full ARN for the role'
)
parser.add_argument(
    '--role-name', help='name of the role', required=True
)
parser.add_argument(
    '--account', help='name of the account'
)
parser.add_argument(
    '--role-session-name', help='the session name', default=None
)

args = parser.parse_args()

def invalid_args():
    print(
        'pass either --role-arn or --role-name and --account', file=sys.stderr
    )
    sys.exit(1)

role_arn = args.role_arn

if role_arn is None:
    if args.role_name is None and args.account is None:
        invalid_args()
    orgs = boto3.client('organizations')
    try:
        accounts = {
            account['Name']: account['Id']
            for page in orgs.get_paginator('list_accounts').paginate()
            for account in page['Accounts']
        }
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    account_id = accounts.get(args.account)
    if account_id is None:
        print(f'unknown account {args.account}', file=sys.stderr)
        sys.exit(1)
    role_arn = f'arn:aws:iam::{account_id}:role/{args.role_name}'
else:
    if args.rone_name is not None or args.account is not None:
        invalid_args()

sts = boto3.client('sts')

if args.role_session_name is not None:
    role_session_name = re.sub(r'[^\w=,.@-]', '-', args.role_session_name)[:64]
else:
    caller_identity = sts.get_caller_identity()
    match = re.search(r':assumed-role/[^/]+/([^/]+)$', caller_identity['Arn'])
    if match is None:
        print(
            f'--role-session-name is required for IAM user credentials',
            file=sys.stderr
        )
        sys.exit(1)
    role_session_name = match.group(1)

try:
    response = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )
except Exception as e:
    print(f'could not assume role {role_arn}:\n\n{e}', file=sys.stderr)
    sys.exit(1)

user = response['AssumedRoleUser']
creds = response['Credentials']

print(
    f"assumed role {role_arn}\n"
    f"    {user['Arn']}\n"
    f"    {user['AssumedRoleId']}",
    file=sys.stderr
)
print(f"export AWS_ACCESS_KEY_ID='{creds['AccessKeyId']}';")
print(f"export AWS_SECRET_ACCESS_KEY='{creds['SecretAccessKey']}';")
print(f"export AWS_SESSION_TOKEN='{creds['SessionToken']}';")
