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
    customer_id = event["CustomerID"]
    if not customer_id:
        return fail()
    delete_customer(cursor, customer_id )
    connection.commit()
    deleted_rows = cursor.rowcount
    cursor.close()
    connection.close()
    return done({"AffectedRows":deleted_rows})

def delete_customer(cursor, customer_id):
    cursor.execute("DELETE from public.\"Customer\" WHERE \"CustomerID\"={0}".format(customer_id))
