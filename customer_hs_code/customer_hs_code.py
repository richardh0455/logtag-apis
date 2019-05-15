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
            value = get_hs_codes(cursor, event.get("CustomerID",""))
        if event.get("Method","")  =="POST":
            value = create_hs_code(cursor,  event.get("CustomerID",""), event.get("HSCode",""))
        if event.get("Method","")  =="PUT":
            value = update_hs_code(cursor, event.get("ID", ""), event.get("CustomerID",""), event.get("HSCode",""))
        if event.get("Method","")  =="DELETE":
            value = delete_hs_code(cursor,  event.get("ID", ""))
        connection.commit()
        cursor.close()
        connection.close()
    except:
        return fail()
    return done(value)



def get_hs_codes(cursor, customer_id):
    cursor.execute("SELECT \"ID\", \"HSCode\"  FROM public.\"CustomerHSCode\" WHERE \"CustomerID\"= %s", (customer_id,))
    list = []
    for row in cursor.fetchall():
        list.append(parse_hs_code(row))
    result = '['
    result += ','.join(list)
    result += ']'
    return result

def parse_hs_code(row):
    result = '{'
    result += "\"ID\":\""+str(row[0])+"\","
    result += "\"HSCode\":\""+row[1]+"\""
    result += '}'
    return result


def create_hs_code(cursor, customer_id, hs_code):
    cursor.execute("INSERT into public.\"CustomerHSCode\" (\"CustomerID\", \"HSCode\")  VALUES ( %s, %s) RETURNING \"ID\"", (customer_id, hs_code,))
    row = cursor.fetchone()
    return {"ID":row[0]}

def update_hs_code(cursor, code_id, customer_id, hs_code):
    cursor.execute("UPDATE public.\"CustomerHSCode\" SET \"CustomerID\"= %s, \"HSCode\"= %s WHERE \"ID\"= %s ", (customer_id, hs_code, code_id,))
    updated_rows = cursor.rowcount
    return {"AffectedRows":updated_rows}

def delete_hs_code(cursor, code_id):
    cursor.execute("DELETE FROM public.\"CustomerHSCode\" WHERE \"ID\"= %s ", (code_id,))
    updated_rows = cursor.rowcount
    return {"AffectedRows":updated_rows}
