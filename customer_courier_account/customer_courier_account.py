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
    updated_rows = 0
    try:
        cursor = connection.cursor()
        if event.get("Method","") =="GET":
            value = get_courier_accounts(cursor, event["CustomerID"])
        if event.get("Method","")  =="POST":
            value = create_courier_account(cursor,  event.get("CustomerID",""), event.get("CourierAccount",""))
        if event.get("Method","")  =="PUT":
            value = update_courier_account(cursor, event.get("AccountID", ""), event.get("CustomerID",""), event.get("CourierAccount",""))
        if event.get("Method","")  =="DELETE":
            value = delete_courier_account(cursor,  event.get("AccountID", ""))
        connection.commit()
        cursor.close()
        connection.close()
    except:
        return fail()
    return done(value)



def get_courier_accounts(cursor, customer_id):
    cursor.execute("SELECT \"ID\", \"CourierAccount\"  FROM public.\"CustomerCourierAccount\" WHERE \"ID\"= {0}".format(account_id))
    list = []
    for row in cursor.fetchall():
        list.append(parse_courier_account(row))
    result = '['
    result += ','.join(list)
    result += ']'
    return result

def parse_courier_account(row):
    result = '{'
    result += "\"ID\":\""+str(row[0])+"\","
    result += "\"CourierAccount\":\""+row[1]+"\""
    result += '}'
    return result


def create_courier_account(cursor, customer_id, courier_account):
    cursor.execute("INSERT into public.\"CustomerCourierAccount\" (\"CustomerID\", \"CourierAccount\")  VALUES ( %s, %s) RETURNING \"ID\"", (customer_id, courier_account))
    row = cursor.fetchone()
    return {"AccountID":row[0]}

def update_courier_account(cursor, account_id, customer_id, courier_account):
    cursor.execute("UPDATE public.\"CustomerCourierAccount\" SET \"CustomerID\"= %s, \"CourierAccount\"= %s WHERE \"ID\"= %s ", (customer_id, courier_account, account_id))
    updated_rows = cursor.rowcount
    return {"AffectedRows":updated_rows}

def delete_courier_account(cursor, account_id):
    cursor.execute("DELETE FROM public.\"CustomerCourierAccount\" WHERE \"ID\"= %s ", (account_id))
    updated_rows = cursor.rowcount
    return {"AffectedRows":updated_rows}
