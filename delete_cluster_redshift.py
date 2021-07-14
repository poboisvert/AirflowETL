import pandas as pd
import boto3
import json

import logging

## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os
 
logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

import configparser
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

def main():
    """
    Description:
        - Sets up a Redshift cluster on AWS
    
    Returns:
        None
    """
    KEY                    = os.getenv("KEY_IAM_AWS")
    SECRET                 = os.getenv("SECRET_IAM_AWS")
    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

    redshift = boto3.client('redshift',
                            region_name="us-east-2",
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)

    iam = boto3.client('iam',
                       region_name='us-east-2',
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET)

    redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  
                            SkipFinalClusterSnapshot=True)
    
    # Remove role:
    iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, 
                           PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
    print("Cluster and IAM role has been deleted")

if __name__ == "__main__":
    main()