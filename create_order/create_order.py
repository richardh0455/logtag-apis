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
    invoice_id = create_invoice(cursor, int(event["customerID"]))
    create_invoice_items(cursor, invoice_id, event["invoiceLines"])
    connection.commit()
    cursor.close()
    connection.close()
    return done(json.dumps('{ \"InvoiceID\":\"'+str(invoice_id)+'\"}'))
    
def create_invoice(cursor, customerID):
    cursor.execute("INSERT into public.\"Invoice\" (\"CustomerID\")  VALUES ( %s ) RETURNING \"InvoiceID\"", [customerID])
    row = cursor.fetchone()
    return row[0]

def create_invoice_items(cursor, invoiceID, invoiceLines):
    
    for line in invoiceLines:
        variationID = line["VariationID"]
        if(line["VariationID"] == "NULL"):
            variationID = "0"
        cursor.execute("INSERT into public.\"InvoiceLine\" (\"InvoiceID\", \"Quantity\", \"ProductID\", \"Pricing\", \"VariationID\")  VALUES ( %s, %s, %s, %s, %s )", (invoiceID, int(line["Quantity"]), int(line["ProductID"]), int(line["Price"]),int(variationID)))    
    