import psycopg2
import json
import os
import logging

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
        if event.get("Method","") =="PUT":
            value = update_order(cursor, int(event["params"]["order-id"]), event["body"])
        elif event.get("Method","")  =="DELETE":
            value = delete_order(cursor, int(event["params"]["order-id"]))
        else:
            return fail()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        logging.exception("Something awful happened!")
        return fail()
    return done(value)


def update_order(cursor, invoice_id, body):
    cursor.execute("UPDATE public.\"Invoice\" SET \"ShippedDate\" = %s, \"PaymentDate\" = %s, \"Currency\" = %s, \"CourierAccountID\" = %s, \"ShippingAddressID\" = %s, \"HSCodeID\" = %s, \"PurchaseOrderID\" = %s WHERE \"InvoiceID\"= %s ", ( body.get("ShippingDate",None), body.get("PaymentDate",None), body["Currency"], int(body["CourierAccountID"]), int(body["ShippingAddressID"]), int(body["HSCodeID"]), int(body["PurchaseOrderNumber"]), invoice_id))
    return {"AffectedRows":cursor.rowcount}

def delete_order(cursor, invoice_id):
    cursor.execute("DELETE from public.\"Invoice\" WHERE \"InvoiceID\"= %s", (invoice_id,))
    return {"AffectedRows":cursor.rowcount}
