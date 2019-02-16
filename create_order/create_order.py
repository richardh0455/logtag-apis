import postgresql
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
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    invoice_id = create_invoice(db, int(event["customerID"]))
    create_invoice_items(db, invoice_id, event["invoiceLines"])
    db.close()
    return done(json.dumps('{ \"InvoiceID\":\"'+str(invoice_id)+'\"}'))
    
def create_invoice(db, customerID):
    insert_invoice = db.prepare("INSERT into public.\"Invoice\" (\"CustomerID\")  VALUES ( $1 ) RETURNING \"InvoiceID\"")
    row = insert_invoice(customerID)
    invoiceID = list(row)[0][0]
    return invoiceID

def create_invoice_items(db, invoiceID, invoiceLines):
    insert_line = db.prepare("INSERT into public.\"InvoiceLine\" (\"InvoiceID\", \"Quantity\", \"ProductID\", \"Pricing\", \"VariationID\")  VALUES ( $1, $2, $3, $4, $5 )")
    for line in invoiceLines:
        variationID = line["VariationID"]
        if(line["VariationID"] == "NULL"):
            variationID = "0"
        insert_line(invoiceID, int(line["Quantity"]), int(line["ProductID"]), int(line["Price"]), int(variationID))
    