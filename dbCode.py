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
    """Your existing function to get all items."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    all_items = []
    scan_kwargs = {}

    while True:
        response = table.scan(**scan_kwargs)
        all_items.extend(response.get('Items', []))
        
        if 'LastEvaluatedKey' not in response:
            break
            
        scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
        
    return all_items

def add_user_to_dynamo(table_name, user_data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    table.put_item(Item=user_data)

def delete_user_from_dynamo(table_name, uid):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    table.delete_item(Key={'uID': uid})

# I also had AI help edit this so I could get it working
def update_user_in_dynamo(table_name, uid, new_username, new_email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    table.update_item(
        Key={'uID': uid},
        UpdateExpression="SET username = :val1, email = :val2",
        ExpressionAttributeValues={
            ':val1': new_username,
            ':val2': new_email
        }
    )

def get_user_from_dynamo(table_name, uid):
    """Fetches a single user's full record from DynamoDB."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'uID': uid})
    return response.get('Item')

def add_item_to_user_in_dynamo(table_name, uid, item_id):
    if not uid or not item_id:
        return

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    table.update_item(
        Key={'uID': str(uid)},
        UpdateExpression="SET #user_items = list_append(if_not_exists(#user_items, :empty_list), :new_item)",
        ExpressionAttributeNames={'#user_items': 'items'},
        ExpressionAttributeValues={
            ':empty_list': [],
            ':new_item': [str(item_id)]
        }
    )

def get_rds_items_by_ids(item_ids):
    if not item_ids:
        return []

    placeholders = ', '.join(['%s'] * len(item_ids))
    query = f"""
        SELECT I.ID, I.description, I.price, C.name AS category_name
        FROM Inventory I 
        JOIN Category C ON I.categoryID = C.categoryID
        WHERE I.ID IN ({placeholders})
    """
    

    int_ids = [int(x) for x in item_ids]
    return execute_query(query, tuple(int_ids))

def remove_item_from_user_in_dynamo(table_name, uid, item_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={'uID': str(uid)})
    user = response.get('Item')
    
    if user and 'items' in user:
        current_items = user['items']
        new_items = [i for i in current_items if str(i) != str(item_id)]

        table.update_item(
            Key={'uID': str(uid)},
            UpdateExpression="SET #user_items = :val",
            ExpressionAttributeNames={'#user_items': 'items'},
            ExpressionAttributeValues={':val': new_items}
        )