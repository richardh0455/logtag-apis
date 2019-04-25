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
        product_id = create_product(cursor, event["Name"],event["Description"],int(event["CostPrice"]) )
        connection.commit()
        cursor.close()
        connection.close()
        return done(json.dumps('{ \"ProductID\":\"'+str(product_id)+'\"}'))
    except:
        return fail()


def create_product(cursor, name, description, cost_price):
    cursor.execute("INSERT into public.\"Product\" (\"Name\", \"Description\", \"CostPrice\" )  VALUES ( %s, %s, %s ) RETURNING \"ProductID\"",(name, description, cost_price))
    row = cursor.fetchone()
    return row[0]
