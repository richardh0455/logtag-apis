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
    if event.get("Method","") =="GET":
        value = get_billing_addresses(cursor, event["params"]["customer-id"])
    elif event.get("Method","")  =="POST":
        value = create_billing_address(cursor, event["body"], event["params"]["customer-id"])
    else:
        return fail()
    connection.commit()
    cursor.close()
    connection.close()
    return done(value)


def create_billing_address(cursor, body, customer_id):
    cursor.execute("INSERT into public.\"CustomerBillingAddress\" (\"CustomerID\", \"Street\", \"Suburb\", \"City\", \"State\", \"Country\", \"PostCode\")  VALUES ( %s, %s, %s, %s, %s, %s, %s) RETURNING \"BillingAddressID\"", (customer_id,  body["Street"],  body["Suburb"],  body["City"],  body["State"],  body["Country"],  body["PostCode"]))
    row = cursor.fetchone()
    return done(json.dumps('{ \"BillingAddressID\":\"'+str(row[0])+'\"}'))

def get_billing_addresses(cursor, customer_id):
    cursor.execute("SELECT \"BillingAddressID\", \"Street\", \"Suburb\", \"City\", \"State\", \"Country\", \"PostCode\" FROM public.\"CustomerBillingAddress\" WHERE \"CustomerID\"= %s", (customer_id,))
    result = '['
    list =[]
    for row in cursor.fetchall():
        address = '{'
        address += "\"ID\": \""+str(row[0])+"\","
        address += '\"Street\": \"' + str(row[1]) + '\",'
        address += '\"Suburb\": \"' + str(row[2]) + '\",'
        address += '\"City\": \"' + str(row[3]) + '\",'
        address += '\"State\": \"' + str(row[4]) + '\",'
        address += '\"Country\": \"' + str(row[5]) + '\",'
        address += '\"PostCode\": \"' + str(row[6]) + '\"'
        address += '}'
        list.append(address)
    result += ','.join(list)
    result += ']'
    return result
