import postgresql
import json


host  = "<ELIDED>"
port = '<ELIDED>'
username = "<ELIDED>"
password = "<ELIDED>"
db_name = "<ELIDED>"


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
    print('Received event: '+json.dumps(event))
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    try:
        customer_id = int(event["id"])
    except:
        console.log('id is not an int');
        return fail()
        
    customer = '{';
    customer += parse_contact_info(db, customer_id)
    customer += ','
    customer += parse_shipping_addresses(db, customer_id)
    customer += '}';
    return done(customer)
    
def parse_row(row):
    result = '{'
    for index, item in enumerate(row.items()):
        if index != 0:
            result += ','
        result += str('\"'+item[0]+'\"') + ':\"' + str(item[1]) + '\"'
    result += '}'
    return result

def parse_contact_info(db, customer_id):
    cursor = db.prepare("SELECT * FROM public.\"Customer\" WHERE \"CustomerID\"="+str(customer_id))
    contact_info = cursor.first()
    result = '\"ContactInfo\": {'
    for index, item in enumerate(contact_info.items()):
        if index != 0:
            result += ','
        result += str('\"'+item[0]+'\"') + ':\"' + str(item[1]) + '\"'
    result += '}'
    return result     
    
def parse_shipping_addresses(db, customer_id):
    cursor = db.prepare("SELECT * FROM public.\"CustomerShippingAddress\" WHERE \"CustomerID\"="+str(customer_id))
    result = '\"ShippingAddresses\": ['
    list =[]
    for row in cursor:
        list.append(parse_row(row))
    result += ','.join(list)
    result += ']'
    return result 
    