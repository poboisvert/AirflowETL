import pandas as pd
import boto3
import json
import os
import logging

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

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
    KEY                    = config.get("AWS", "KEY_IAM_AWS")
    SECRET                 = config.get("AWS", "SECRET_IAM_AWS")
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