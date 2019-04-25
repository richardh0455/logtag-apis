import psycopg2
import json
import os
from decimal import Decimal
host  = os.environ['RDS_HOST']
port = os.environ['PORT']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']

def done(response):
    return {
        'statusCode': '200',
        'body': response,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'
        }
    }
def fail():
    return {
        'statusCode': '406',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'
        }
    }

def lambda_handler(event, context):
    connection = psycopg2.connect(user=username,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=db_name)
    updated_rows = 0
    try:
        cursor = connection.cursor()
        update_product(cursor, event["ProductID"], event["Name"],event["Description"],Decimal(event["CostPrice"]) )
        connection.commit()
        updated_rows = cursor.rowcount
        cursor.close()
        connection.close()
    except:
        return fail()

    return done({"AffectedRows":updated_rows})

def update_product(cursor, productID, name, description, cost_price):
    cursor.execute("UPDATE public.\"Product\" SET \"Name\"= %s, \"Description\"= %s, \"CostPrice\"= %s WHERE \"ProductID\"= %s ", (name, description, cost_price, productID))
