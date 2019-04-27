import psycopg2
import json
import os

host  = os.environ['RDS_HOST']
port = os.environ['PORT']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
connection = psycopg2.connect(user=username,
                              password=password,
                              host=host,
                              port=port,
                              database=db_name)


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
    cursor = connection.cursor()
    statement = "SELECT \"InvoiceID\", \"LogtagInvoiceNumber\",\"CreatedDate\" FROM public.\"Invoice\""
    if event.get("CustomerID", "").strip() :
        statement += " WHERE \"CustomerID\"="+event["CustomerID"]
    try:
        cursor.execute(statement)
    except:
        return fail()
    list = []
    for row in cursor.fetchall():
        list.append(parse_row(row))
    result = '['
    result += ','.join(list)
    result += ']'
    connection.commit()
    cursor.close()
    return done(result)

def parse_row(row):
    result = '{'
    result += "\"InvoiceID\":\""+str(row[0])+"\","
    result += "\"CustomerID\":\""+str(row[1])+"\","
    result += "\"CreatedDate\":\""+str(row[2])+"\""
    result += '}'
    return result
