import pandas as pd
import boto3
import json

import logging
 
logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')


import configparser
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

KEY                    = config.get("AWS", "KEY_IAM_AWS")
SECRET                 = config.get("AWS", "SECRET_IAM_AWS")

DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_DB                 = config.get("DWH","DWH_DB")
DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
DWH_PORT               = config.get("DWH","DWH_PORT")

DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

ec2 = boto3.resource('ec2',
                    region_name="us-east-2",
                    aws_access_key_id=KEY,
                    aws_secret_access_key=SECRET
                    )

s3 = boto3.resource('s3',
                    region_name="us-east-2",
                    aws_access_key_id=KEY,
                    aws_secret_access_key=SECRET
                )

iam = boto3.client('iam',aws_access_key_id=KEY,
                    aws_secret_access_key=SECRET,
                    region_name='us-east-2'
                )

redshift = boto3.client('redshift',
                    region_name="us-east-2",
                    aws_access_key_id=KEY,
                    aws_secret_access_key=SECRET
                    )

def create_iam_role():
    """
    Description:
        - Creates an IAM role that allows Redshift to call on 
          other AWS services
    
    Return:
        - roleArn
    """

    # Create the IAM role
    try:
        print('1.1 Creating a new IAM Role')
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description='Allows Redshift clusters to call AWS services on your behalf.',
            AssumeRolePolicyDocument=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "redshift.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                    }
                ]
                }),
        )
        
    except Exception as e:
        print(e)

    print('1.2 Attaching Policy')
    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                        PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                        )['ResponseMetadata']['HTTPStatusCode']

    print('1.3 Get the IAM role ARN')
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

    print("Please add to dwh.cfg :",roleArn)
    return roleArn

def main():
    """
    Description:
        - Sets up a Redshift cluster on AWS
    
    Returns:
        None
    """

    sampleDbBucket =  s3.Bucket("awssampledbuswest2") # From AWS Documentation sample

    for obj in sampleDbBucket.objects.filter(Prefix="ssbgz"):
        print (obj)

    roleArn = create_iam_role()
        
    try:
        response = redshift.create_cluster(        
            #HW
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),

            #Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,
            
            #Roles (for s3 access)
            IamRoles=[roleArn]  
        )
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()