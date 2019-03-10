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
    customer_id = create_customer(db, event["Name"],event["EmailAddress"],event["BillingAddress"], event["Region"] )
    db.close()
    return done(json.dumps('{ \"CustomerID\":\"'+str(customer_id)+'\"}'))
    
def create_customer(db, name, email, billing_address, region):
    create_customer = db.prepare("INSERT into public.\"Customer\" (\"Name\", \"Contact_Email\", \"Billing_Address\", \"Region\" )  VALUES ( $1, $2, $3, $4 ) RETURNING \"CustomerID\"")
    row = create_customer(name, email, billing_address, region)
    customer_id = list(row)[0][0]
    return customer_id

    