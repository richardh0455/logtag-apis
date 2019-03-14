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
    try:
        customer_id = int(event["id"])
    except:
        console.log('id is not an int');
        return fail()
        
    customer = '{';
    customer += parse_contact_info(cursor, customer_id)
    customer += ','
    customer += parse_shipping_addresses(cursor, customer_id)
    customer += '}';
    connection.commit()
    cursor.close()
    return done(customer)
    

def parse_contact_info(cursor, customer_id):
    cursor.execute("SELECT \"Name\", \"Contact_Email\", \"Billing_Address\", \"Region\"  FROM public.\"Customer\" WHERE \"CustomerID\"= %s",(str(customer_id),))
    row = cursor.fetchone()
    result = '\"ContactInfo\": {'
    result += "\"Name\": \""+str(row[0])+"\"," + '\"Contact_Email\": \"' + str(row[1]) + '\",' + '\"Billing_Address\": \"' + str(row[2]) + '\",' + '\"Region\": \"' + str(row[3]) + '\"' 
    result += '}'
    return result     
    
def parse_shipping_addresses(cursor, customer_id):
    cursor.execute("SELECT \"ShippingAddressID\", \"ShippingAddress\" FROM public.\"CustomerShippingAddress\" WHERE \"CustomerID\"= %s", (str(customer_id),))
    result = '\"ShippingAddresses\": ['
    list =[]
    for row in cursor.fetchall():
        result = '{'
        result += "\"ID\": \""+str(row[0])+"\"," + '\"ShippingAddress\": \"' + str(row[1]) + '\"'
        result += '}'
    result += ','.join(list)
    result += ']'
    return result 
    