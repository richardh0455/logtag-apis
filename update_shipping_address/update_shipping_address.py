import psycopg2
import json
import os

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

def lambda_handler(event, context):
    connection = psycopg2.connect(user=username,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=db_name)
    cursor = connection.cursor()
    update_shipping_address(cursor, event["ShippingAddressID"],event["ShippingAddress"])
    connection.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    connection.close()
    return done({"AffectedRows":updated_rows})

def update_shipping_address(cursor, shipping_address_id, shipping_address):
    cursor.execute("UPDATE public.\"CustomerShippingAddress\" SET \"ShippingAddress\"=%s WHERE \"ShippingAddressID\" =%s", (shipping_address, shipping_address_id))
