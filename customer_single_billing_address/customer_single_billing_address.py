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
    cursor = connection.cursor()
    if event.get("Method","") =="PUT":
        value = update_shipping_address(cursor, event["params"]["billing-address-id"], event["params"]["customer-id"], event["body"])
    elif event.get("Method","")  =="DELETE":
        value = delete_shipping_address(cursor, event["params"]["billing-address-id"], event["params"]["customer-id"])
    else:
        return fail()
    connection.commit()
    cursor.close()
    connection.close()
    return done(value)

def update_shipping_address(cursor, billing_address_id, customer_id,  body):
    cursor.execute("UPDATE public.\"CustomerBillingAddress\" SET \"Street\"=%s,\"Suburb\"=%s,\"City\"=%s,\"State\"=%s,\"Country\"=%s,\"PostCode\"=%s WHERE \"BillingAddressID\" =%s AND \"CustomerID\" =%s", (body["Street"],body["Suburb"],body["City"],body["State"],body["Country"],body["PostCode"], billing_address_id, customer_id))
    return {"AffectedRows":cursor.rowcount}

def delete_shipping_address(cursor, billing_address_id, customer_id):
    cursor.execute("DELETE from public.\"CustomerBillingAddress\" WHERE \"BillingAddressID\" = %s AND \"CustomerID\" = %s", (billing_address_id, customer_id))
    return {"AffectedRows":cursor.rowcount}
