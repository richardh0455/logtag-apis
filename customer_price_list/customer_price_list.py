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
            value = get_price_lists(cursor, event.get("CustomerID",""), event.get("ProductID",""))
        if event.get("Method","")  =="POST":
            value = create_price_item(cursor,  event.get("CustomerID",""), event.get("ProductID",""), event.get("Price",""), event.get("Lower_Range",""), event.get("Upper_Range",""))
        if event.get("Method","")  =="PUT":
            value = update_price_item(cursor, event.get("ID", ""), event.get("CustomerID",""), event.get("ProductID",""), event.get("Price",""), event.get("Lower_Range",""), event.get("Upper_Range",""))
        if event.get("Method","")  =="DELETE":
            value = delete_price_item(cursor,  event.get("ID", ""))
        connection.commit()
        cursor.close()
        connection.close()
    except:
        return fail()
    return done(value)



def get_price_lists(cursor, customer_id, product_id):
    cursor.execute("SELECT \"ID\", \"Price\", \"Lower_Range\", \"Upper_Range\"  FROM public.\"CustomerPriceList\" WHERE \"CustomerID\"= %s AND ProductID = %s", (customer_id, product_id,))
    list = []
    for row in cursor.fetchall():
        list.append(parse_price_item(row))
    result = '['
    result += ','.join(list)
    result += ']'
    return result

def parse_price_item(row):
    result = '{'
    result += "\"ID\":\""+str(row[0])+"\","
    result += "\"Price\":\""+row[1]+"\","
    result += "\"Lower_Range\":\""+row[2]+"\","
    result += "\"Upper_Range\":\""+row[3]+"\","
    result += '}'
    return result


def create_price_item(cursor, customer_id, product_id, price, lower_range, upper_range):
    cursor.execute("INSERT into public.\"CustomerPriceList\" (\"CustomerID\", \"ProductID\", \"Price\", \"Lower_Range\", \"Upper_Range\")  VALUES ( %s, %s, %s, %s, %s) RETURNING \"ID\"", (customer_id, product_id, price, lower_range, upper_range,))
    row = cursor.fetchone()
    return {"ID":row[0]}

def update_price_item(cursor, item_id, customer_id, product_id, price, lower_range, upper_range):
    cursor.execute("UPDATE public.\"CustomerPriceList\" SET \"CustomerID\"= %s, \"ProductID\"= %s, \"Price\"= %s, \"Lower_Range\"= %s, \"Upper_Range\"= %s WHERE \"ID\"= %s ", (customer_id, product_id, price, lower_range, upper_range, item_id,))
    updated_rows = cursor.rowcount
    return {"AffectedRows":updated_rows}

def delete_price_item(cursor, item_id):
    cursor.execute("DELETE FROM public.\"CustomerPriceList\" WHERE \"ID\"= %s ", (item_id,))
    updated_rows = cursor.rowcount
    return {"AffectedRows":updated_rows}
