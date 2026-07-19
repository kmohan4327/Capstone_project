# Phase 2: Boto3 S3 Upload Flow

This document explains how the Phase 2 notebook uses boto3 to place files into an S3 bucket and how the upload path is constructed.

## High-Level Flow

1. Configure AWS credentials locally using AWS CLI.
2. Load environment variables from a `.env` file.
3. Initialize boto3 clients for IAM, STS, S3, and CloudWatch Logs.
4. Create or verify IAM policies.
5. Configure the target S3 bucket and upload files.
6. Verify the uploaded objects in S3.

## Local AWS CLI and Environment Setup

The notebook expects AWS credentials to be available locally. It uses the AWS CLI configuration process:

```bash
aws configure
```

The following fields are typically set:

- AWS Access Key ID
- AWS Secret Access Key
- Default region name (`us-east-1`)
- Default output format (`json`)

The notebook also loads values from a `.env` file using `dotenv`:

```python
import os
from dotenv import load_dotenv
import boto3
load_dotenv()
my_bucket_name = os.getenv("AWS_BUCKET_NAME")
```

Environment variables include:

- `AWS_BUCKET_NAME` or `AWS_TARGET_BUCKET`
- `AWS_REGION`

## Boto3 Client Initialization

The notebook creates boto3 clients for AWS services:

- IAM: `boto3.client("iam")`
- STS: `boto3.client("sts")`
- S3: `boto3.client('s3', region_name=os.getenv("AWS_REGION"))`
- CloudWatch Logs: `boto3.client('logs', region_name=os.getenv("AWS_REGION"))`

## IAM Policy Creation

The notebook programmatically creates a customer-managed IAM policy with permissions to manage S3 and CloudWatch Logs:

```python
policy_doc = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:*", "logs:*"],
        "Resource": "*"
    }]
}
```

This policy is created with the name:

```python
policy_name = f"boto3-S3logs-mohank-Policy"
```

## Bucket Access and Public Policy

The notebook demonstrates how to update bucket public access settings and attach a bucket policy to allow `s3:GetObject` for all principals.

It calls:

```python
s3_client.put_public_access_block(
    Bucket=TARGET_BUCKET,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': False,
        'IgnorePublicAcls': False,
        'BlockPublicPolicy': False,
        'RestrictPublicBuckets': False
    }
)
```

Then it attaches a bucket policy that allows public read access to all objects:

```python
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{TARGET_BUCKET}/*"
        }
    ]
}
```

## Uploading Files to S3

The notebook defines a list of files under the local `data/` folder:

```python
files = [
    "data/clickstream_day1.json",
    "data/clickstream_day2.json",
    "data/customers.csv",
    "data/order_items_day1.json",
    "data/order_items_day2.json",
    "data/orders_day1.json",
    "data/orders_day2.json",
    "data/products.csv"
]
```

It uploads these files using the `upload_file` method:

```python
for file in files:
    s3_client.upload_file(file, target_bucket, f"raw/{file}")
```

### Resulting S3 Object Keys

Because each file path includes the `data/` directory and the upload prefix is `raw/`, the resulting object keys are:

- `raw/data/clickstream_day1.json`
- `raw/data/clickstream_day2.json`
- `raw/data/customers.csv`
- `raw/data/order_items_day1.json`
- `raw/data/order_items_day2.json`
- `raw/data/orders_day1.json`
- `raw/data/orders_day2.json`
- `raw/data/products.csv`

So the files are placed in S3 under the `raw/` prefix and retain their local `data/` subfolder structure.

## Verifying Uploaded Objects

The notebook also includes a verification helper using `list_objects_v2`:

```python
response = s3_client.list_objects_v2(Bucket=target_bucket, Prefix=prefix)
```

It verifies the bucket contents under the `raw/data/` prefix to confirm uploads succeeded.

## CloudWatch Logging

The notebook sets up CloudWatch Logs to record pipeline execution events.

It creates a log group and stream if needed, then sends messages like:

- "CloudWatch setup complete. Ready for pipeline execution."
- "File successfully uploaded to {target_bucket}/{object_name}"
- "S3 Utility script execution completed successfully."

This provides auditability and visibility into the upload process.

## Summary

The notebook places the entire boto3-based upload utility in the following logical order:

1. Configure AWS credentials and load environment variables.
2. Initialize boto3 clients for AWS services.
3. Create or validate IAM policy and bucket settings.
4. Upload local data files to the S3 `raw/` prefix.
5. Verify the uploaded objects.
6. Send execution logs to CloudWatch.

The uploaded files land in S3 with object keys that preserve the local `data/` folder structure under `raw/`.
