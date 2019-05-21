import botocore.session
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
    session = botocore.session.get_session()
    client = session.create_client("quicksight", region_name='ap-southeast-2')
    dashboard_url = client.get_dashboard_embed_url(AwsAccountId="276219036989", DashboardId="48187bc4-17ee-4a2c-b474-e69e184bd270", IdentityType="IAM", SessionLifetimeInMinutes=100, ResetDisabled=True, UndoRedoDisabled=True)
    result = '{'
    result += 'URL:'
    result += dashboard_url
    result += '}'

    return done(result)
