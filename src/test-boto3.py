
import boto3
import logging
from botocore.exceptions import ClientError
import os

def create_bucket(bucket_name, region = None):

    try:
        if region is None:
            s3_client = boto3.client("s3")
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client("s3", region_name=region)
            location = {"LocationConstraint": region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration = location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(file_name, bucket, object_name=None):
    
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# if I don't put in region, it gives me IllegalLocationConstraintException since default region
# is not us-east-1, and for the s3 api needs locationconstraint set if region is not us-east-1,
# although shouldn't boto3 recognize my default region is not that and set locationconstraint 
# appropriately?
bucket_name = "twedl-edgar-ex-1"
# create_bucket(bucket_name, region = "ca-central-1")

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)


# upload file: what does this have to do with the upload_file method from the tutorial?
# object_name => None, take from filename?
file_name = "tests/data/9999999997-22-000180.nc"
s3_client = boto3.client("s3")
with open(file_name, "rb") as f:
    s3_client.upload_fileobj(f, bucket_name, os.path.basename(file_name)) 

# huh, that worked huh




# alright, so plan: think of index, folder strategy for .nc files? 
# then...idk...move them all over there? then process from there?
# or download...process...idk. consider transfer costs.


# alright, think about wtf im going to do here

