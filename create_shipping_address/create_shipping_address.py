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
    shipping_address_id = create_shipping_address(cursor, event["CustomerID"],event["ShippingAddress"])
    connection.commit()
    cursor.close()
    connection.close()
    return done(json.dumps('{ \"ShippingAddressID\":\"'+str(shipping_address_id)+'\"}'))
    
def create_shipping_address(cursor, customer_id, shipping_address):
    create_shipping_address = cursor.execute("INSERT into public.\"CustomerShippingAddress\" (\"CustomerID\", \"ShippingAddress\")  VALUES ( %s, %s) RETURNING \"ShippingAddressID\"", (customer_id, shipping_address))
    row = cursor.fetchone()
    return row[0]

    