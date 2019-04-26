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
        update_variation(cursor, event["Description"], event["CustomerID"],event["ProductID"],Decimal(event["Price"]),event["ConfigurationID"] )
        connection.commit()
        updated_rows = cursor.rowcount
        cursor.close()
        connection.close()
    except:
        return fail()

    return done({"AffectedRows":updated_rows})

def update_variation(cursor, description, customer_id, product_id, price, configuration_id):
    cursor.execute("UPDATE public.\"ProductConfiguration\" SET \"Description\"= %s, \"CustomerID\"= %s, \"ProductID\"= %s, \"Price\"= %s WHERE \"ConfigurationID\"= %s ", (description, customer_id, product_id, price, configuration_id))
