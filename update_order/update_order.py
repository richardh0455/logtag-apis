import psycopg2
import json
import os
from decimal import Decimal
from psycopg2.extensions import AsIs

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
        shipping_date = event.get("ShippingDate","")
        if shipping_date.strip():
            update_order(cursor, event["OrderID"],'ShippedDate',shipping_date )

        purchase_date = event.get("PurchaseDate","")
        if purchase_date.strip():
            update_order(cursor, event["OrderID"],"PaymentDate", purchase_date)
        connection.commit()
        updated_rows = cursor.rowcount
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return fail()

    return done({"AffectedRows":updated_rows})

def update_order(cursor, orderID, fieldName, fieldValue):
    cursor.execute("UPDATE public.\"Invoice\" SET \"%s\" = %s WHERE \"InvoiceID\"= %s ", (AsIs(fieldName), fieldValue, orderID))
