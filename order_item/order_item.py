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

    try:
        cursor = connection.cursor()
        if event.get("Method","")  =="PUT":
            value = update_order_item(cursor, event["params"]["line-id"], event["params"]["order-id"], event["body"])
        elif event.get("Method","")  =="DELETE":
            value = delete_order_item(cursor, event["params"]["line-id"], event["params"]["order-id"])
        else:
            return fail()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return fail()
    return done(value)


def update_order_item(cursor, line_id, order_id, item):
    variationID = item["VariationID"]
    if(item["VariationID"] == "NULL" or item["VariationID"] == "None" ):
        variationID = "0"
    cursor.execute("UPDATE public.\"InvoiceLine\" SET \"Quantity\" = %s, \"ProductID\" = %s, \"Pricing\" = %s, \"VariationID\" = %s WHERE \"LineID\"= %s AND \"InvoiceID\"= %s", (int(item["Quantity"]), int(item["ProductID"]), Decimal(item["Price"]),int(variationID), int(line_id), int(order_id)))
    return {"AffectedRows":cursor.rowcount}

def delete_order_item(cursor, line_id, order_id):
    cursor.execute("DELETE from public.\"InvoiceLine\" WHERE \"LineID\"= %s AND \"InvoiceID\"= %s", (int(line_id), int(order_id)))
    return {"AffectedRows":cursor.rowcount}
