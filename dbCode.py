# dbCode.py
# Author: Your Name
# Helper functions for database connection and queries
#

import pymysql
import creds
import boto3

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def scan_all_items(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    all_items = []
    scan_kwargs = {}

    while True:
        response = table.scan(**scan_kwargs)
        all_items.extend(response.get('Items', []))
        
        # Check if there are more pages
        if 'LastEvaluatedKey' not in response:
            break
            
        # Set the exclusive start key for the next iteration
        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        
    return all_items