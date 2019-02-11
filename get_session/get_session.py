import boto3
import json
import decimal

dynamodb = boto3.client('dynamodb')

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
    try:
        state = json.dumps(event["state"])
        result = dynamodb.get_item(TableName='logtag-sessions', Key={'SESSION_KEY':{'S':event["session_key"]}})
        parsed_result = json.loads(result["Item"]["STATE"]["S"])
        return done(parsed_result)
    except Exception as e:
        print(e)
        return fail()
    