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
        if event.get("Method","") =="POST":
            value = create_order_item(cursor, int(event["params"]["order-id"]), event["body"])
        elif event.get("Method","") =="GET":
            value = get_order_items(cursor, int(event["params"]["order-id"]))
        else:
            return fail()
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return fail()
    return done(value)

def create_order_item(cursor, invoice_id, item):
    variationID = item["VariationID"]
    if(line["VariationID"] == "NULL"):
        variationID = "0"
    cursor.execute("INSERT into public.\"InvoiceLine\" (\"InvoiceID\", \"Quantity\", \"ProductID\", \"Pricing\", \"VariationID\")  VALUES ( %s, %s, %s, %s, %s )", (invoice_id, int(item["Quantity"]), int(item["ProductID"]), Decimal(item["Price"]),int(variationID)))
    return {"AffectedRows":cursor.rowcount}

def get_order_items(cursor, invoice_id):
    cursor.execute("SELECT \"ProductID\", \"VariationID\", \"Pricing\", \"Quantity\" FROM public.\"InvoiceLine\" WHERE \"InvoiceID\"= %s",(invoice_id,))
    result = '\"OrderLines\": ['
    list =[]
    for row in cursor.fetchall():
        line = '{'
        line += "\"ProductID\": \""+str(row[0])+"\"," +"\"VariationID\": \""+str(row[1])+"\"," +"\"Pricing\": \""+str(row[2])+"\"," + '\"Quantity\": \"' + str(row[3]) + '\"'
        line += '}'
        list.append(line)
    result += ','.join(list)
    result += ']'
    return result
