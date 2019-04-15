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
    try:
        invoice_id = int(event["OrderID"])
    except:
        return fail()

    order = '{';
    order += parse_order_metadata(cursor, invoice_id)
    order += ','
    order += parse_order_lines(cursor, invoice_id)
    order += '}';

    connection.commit()
    cursor.close()
    connection.close()
    return done(order)

def parse_order_metadata(cursor, invoice_id):
    cursor.execute("SELECT CustomerID, ShippedDate,PaymentDate,LogtagInvoiceNumber FROM public.\"Invoice\" WHERE \"InvoiceID\"= %s",(str(id),))
    row = cursor.fetchone()
    result = '\"Order\": {'
    result += "\"CustomerID\": \""+str(row[0])+"\"," + '\"ShippedDate\": \"' + str(row[1]) + '\",' + '\"PaymentDate\": \"' + str(row[2]) + '\",' + '\"LogtagInvoiceNumber\": \"' + str(row[3]) + '\"'
    result += '}'
    return result;

def parse_order_lines(cursor, invoice_id):
    cursor.execute("SELECT ProductID, VariationID, Pricing, Quantity FROM public.\"InvoiceLine\" WHERE \"InvoiceID\"= %s",(str(id),))
    result = '\"OrderLines\": ['
    list =[]
    for row in cursor.fetchall():
        line = '{'
        line += "\"ProductID\": \""+str(row[0])+"\"," +"\"VariationID\": \""+str(row[1])+"\"," +"\"Pricing\": \""+str(row[2])+"\"," + '\"Quantity\": \"' + str(row[3]) + '\"'
        line += '}'
        list.append(line)
    result += ','.join(list)
    result += ']'
    return result
