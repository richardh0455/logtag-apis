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

def lambda_handler(event, context):
    cursor = connection.cursor()
    customer_id = event["CustomerID"]
    product_id = event["ProductID"]
    cursor.execute("SELECT \"ConfigurationID\", \"Description\", \"Price\" FROM public.\"ProductConfiguration\" WHERE \"CustomerID\"= %s AND \"ProductID\"= %s",(str(customer_id),str(product_id),))
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
    result += "\"VariantID\":\""+str(row[0])+"\","
    result += "\"Description\":\""+row[1]+"\","
    result += "\"Price\":\""+str(row[2])+"\""
    result += '}'
    return result  
