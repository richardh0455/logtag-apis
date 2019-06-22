import psycopg2
import json
import os
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

    try:
        cursor = connection.cursor()
        if event.get("Method","") =="GET":
            value = get_products(cursor)
        elif event.get("Method","")  =="POST":
            value = create_product(cursor, event["body"])
        else:
            return fail()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return fail()
    return done(value)


def create_product(cursor, body):
    cursor.execute("INSERT into public.\"Product\" (\"Name\", \"Description\", \"CostPrice\" )  VALUES ( %s, %s, %s ) RETURNING \"ProductID\"",(body["Name"], body["Description"], Decimal(body["CostPrice"])))
    row = cursor.fetchone()
    return {'ProductID':row[0]}


def get_products(cursor):
    cursor.execute("SELECT \"ProductID\", \"Name\", \"Description\",\"CostPrice\" FROM public.\"Product\"")
    list = []
    for row in cursor.fetchall():
        list.append(parse_row(row))
    result = '['
    result += ','.join(list)
    result += ']'
    return done(result)

def parse_row(row):
    result = '{'
    result += "\"ProductID\":\""+str(row[0])+"\","
    result += "\"Name\":\""+row[1]+"\","
    result += "\"Description\":\""+row[2]+"\","
    result += "\"Cost_Price\":\""+str(row[3])+"\""
    result += '}'
    return result
