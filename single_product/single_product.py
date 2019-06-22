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
        if event.get("Method","") =="PUT":
            value = update_product(cursor, int(event["params"]["product-id"]), event["body"])
        elif event.get("Method","")  =="DELETE":
            value = delete_product(cursor, int(event["params"]["product-id"]))
        else:
            return fail()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return fail()
    return done(value)

def update_product(cursor, productID, body):
    cursor.execute("UPDATE public.\"Product\" SET \"Name\"= %s, \"Description\"= %s, \"CostPrice\"= %s WHERE \"ProductID\"= %s ", (body["Name"], body["Description"], Decimal(body["CostPrice"]), productID))
    return {"AffectedRows":cursor.rowcount}

def delete_product(cursor, product_id):
    cursor.execute("DELETE from public.\"Product\" WHERE \"ProductID\"= %s", (product_id,))
    return {"AffectedRows":cursor.rowcount}
