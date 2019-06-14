import psycopg2
import json
import os
from datetime import datetime

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
        if event.get("Method","") =="GET":
            value = get_orders(cursor, event["query"])
        elif event.get("Method","")  =="POST":
            value = create_order(cursor, event["body"])
        else:
            return fail()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return fail()
    return done(value)

def get_orders(cursor, queryParams):
    if('customer-id' in queryParams):
        get_orders_by_customer(cursor, int(queryParams["customer-id"]))
    else:
        get_all_orders(cursor)
    orders = [];
    for row in cursor.fetchall():
        result = '{'
        result += "\"CustomerID\": \""+str(row[0])+"\","
        result += '\"ShippedDate\": \"' + str(row[1]) + '\",'
        result += '\"PaymentDate\": \"' + str(row[2]) + '\",'
        result += '\"LogtagInvoiceNumber\": \"' + str(row[3]) + '\",'
        result += '\"Currency\": \"' + str(row[4]) + '\",'
        result += '\"PurchaseOrderNumber\": \"' + str(row[5]) + '\",'
        result += '\"InvoiceID\": \"' + str(row[6]) + '\",'
        result += '\"CourierAccountID\": \"' + str(row[7]) + '\",'
        result += '\"HSCodeID\": \"' + str(row[8]) + '\",'
        result += '\"ShippingAddressID\": \"' + str(row[9]) + '\",'
        result += '\"BillingAddressID\": \"' + str(row[10]) + '\"'
        result += '}'
        orders.append(result)
    return '['+','.join(orders)+']'

def get_all_orders(cursor):
    cursor.execute("SELECT \"CustomerID\", \"ShippedDate\", \"PaymentDate\", \"LogtagInvoiceNumber\", \"Currency\", \"PurchaseOrderID\", \"InvoiceID\", \"CourierAccountID\", \"HSCodeID\", \"ShippingAddressID\", \"BillingAddressID\"  FROM public.\"Invoice\"")

def get_orders_by_customer(cursor, customer_id):
    cursor.execute("SELECT \"CustomerID\", \"ShippedDate\", \"PaymentDate\", \"LogtagInvoiceNumber\", \"Currency\", \"PurchaseOrderID\", \"InvoiceID\", \"CourierAccountID\", \"HSCodeID\", \"ShippingAddressID\", \"BillingAddressID\" FROM public.\"Invoice\" WHERE \"CustomerID\"= %s",(str(customer_id),))

def create_order(cursor, body):
    count = generate_invoice_number(cursor)
    logtagInvoiceNumber = 'IN'+datetime.now().strftime("%y%m%d")+'-'+str(count).zfill(2)
    cursor.execute("INSERT into public.\"Invoice\" (\"CustomerID\", \"LogtagInvoiceNumber\", \"Currency\", \"PurchaseOrderID\",\"CourierAccountID\",\"HSCodeID\", \"ShippingAddressID\" )  VALUES ( %s, %s, %s, %s, %s, %s ) RETURNING \"InvoiceID\"", ( int(body['CustomerID']), logtagInvoiceNumber, body['Currency'], body['PurchaseOrderNumber'], int(body['CourierAccountID']), int(body['HSCodeID']), int(body['ShippingAddressID'])))
    row = cursor.fetchone()
    return {"InvoiceID":row[0], "LogtagInvoiceNumber":logtagInvoiceNumber}

def generate_invoice_number(cursor):
    cursor.execute("SELECT COUNT(*) FROM public.\"Invoice\" WHERE \"Created_At\"> now() - interval '1 day' ")
    row = cursor.fetchone()
    if row is None:
        return 1
    return row[0]+1;
