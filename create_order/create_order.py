import psycopg2
import json
import os
from datetime import datetime
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
    cursor = connection.cursor()
    logtagInvoiceNumber = 'IN'+datetime.now().strftime("%d%m%y")
    try:
        invoice_id = create_invoice(cursor, int(event["customerID"]), logtagInvoiceNumber, event["purchaseOrderNumber"])
        create_invoice_items(cursor, invoice_id, event["invoiceLines"])
    except:
        return fail()
    connection.commit()
    cursor.close()
    connection.close()
    return done(json.dumps('{ \"InvoiceID\":\"'+str(invoice_id)+'\",  \"LogtagInvoiceNumber\":\"'+str(logtagInvoiceNumber)+'\"}'))

def create_invoice(cursor, customerID, logtagInvoiceNumber, purchaseOrderNumber):

    cursor.execute("INSERT into public.\"Invoice\" (\"CustomerID\", \"LogtagInvoiceNumber\", \"PurchaseOrderID\")  VALUES ( %s, %s, %s ) RETURNING \"InvoiceID\"", [customerID, logtagInvoiceNumber,purchaseOrderNumber])
    row = cursor.fetchone()
    return row[0]

def create_invoice_items(cursor, invoiceID, invoiceLines):

    for line in invoiceLines:
        variationID = line["VariationID"]
        if(line["VariationID"] == "NULL"):
            variationID = "0"
        cursor.execute("INSERT into public.\"InvoiceLine\" (\"InvoiceID\", \"Quantity\", \"ProductID\", \"Pricing\", \"VariationID\")  VALUES ( %s, %s, %s, %s, %s )", (invoiceID, int(line["Quantity"]), int(line["ProductID"]), Decimal(line["Price"]),int(variationID)))
