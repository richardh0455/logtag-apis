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

    try:
        cursor = connection.cursor()
        if event.get("Method","") =="GET":
            value = get_orders(cursor, int(event["query"]["customer-id"]))
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

def get_orders(cursor, customer_id):
    orders = '{[';
    cursor.execute("SELECT \"CustomerID\", \"ShippedDate\", \"PaymentDate\", \"LogtagInvoiceNumber\" FROM public.\"Invoice\" WHERE \"CustomerID\"= %s",(str(customer_id)))
    for row in cursor.fetchall():
        result = '{'
        result += "\"CustomerID\": \""+str(row[0])+"\"," + '\"ShippedDate\": \"' + str(row[1]) + '\",' + '\"PaymentDate\": \"' + str(row[2]) + '\",' + '\"LogtagInvoiceNumber\": \"' + str(row[3]) + '\"'
        result += '},'
    orders += ']}'
    return order

def update_order(cursor, invoice_id, body):
    cursor.execute("UPDATE public.\"Invoice\" SET \"CustomerID\" = %s, \"ShippedDate\" = %s, \"PaymentDate\" = %s, \"LogtagInvoiceNumber\" = %s WHERE \"InvoiceID\"= %s ", (int(body["CustomerID"]), body["ShippedDate"], body["PaymentDate"], body["LogtagInvoiceNumber"], invoice_id))
    return {"AffectedRows":cursor.rowcount}


def create_order(cursor, body):
    count = generate_invoice_number(cursor)
    logtagInvoiceNumber = 'IN'+datetime.now().strftime("%y%m%d")+'-'+str(count).zfill(2)
    cursor.execute("INSERT into public.\"Invoice\" (\"CustomerID\", \"LogtagInvoiceNumber\")  VALUES ( %s, %s ) RETURNING \"InvoiceID\"", [int(body['CustomerID']), logtagInvoiceNumber])
    row = cursor.fetchone()
    return row[0]

def generate_invoice_number(cursor):
    cursor.execute("SELECT COUNT(*) FROM public.\"Invoice\" WHERE \"Created_At\"> now() - interval '1 day' ")
    row = cursor.fetchone()
    if row is None:
        return 1
    return row[0]+1;
