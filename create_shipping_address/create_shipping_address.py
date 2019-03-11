import postgresql
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

def lambda_handler(event, context):
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    shipping_address_id = create_shipping_address(db, event[""],event[""],event[""], event[""] )
    db.close()
    return done(json.dumps('{ \"CustomerID\":\"'+str(shipping_address_id)+'\"}'))
    
def create_shipping_address(db, name, email, billing_address, region):
    create_shipping_address = db.prepare("INSERT into public.\"Shipping_Address\" (\"Name\", \"Contact_Email\", \"Billing_Address\", \"Region\" )  VALUES ( $1, $2, $3, $4 ) RETURNING \"ShippingAddressID\"")
    row = create_shipping_address(name, email, billing_address, region)
    shipping_address_id = list(row)[0][0]
    return shipping_address_id

    