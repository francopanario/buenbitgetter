import json
import requests
from datetime import datetime
import pytz
import boto3


def lambda_handler(event, context):
    response = requests.get('https://be.buenbit.com/api/market/tickers/')
    if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
        my_dict = json.loads(response.content.decode('utf-8'))
        today = datetime.now(tz=pytz.UTC)
        today_day=today.strftime(format='%Y-%m-%d')
        today_time=today.strftime(format='%H:%M:%S')
        filename='buenbit_fx'+today.strftime(format='%Y%m%d%H%M%S')+'.json'
        my_dict['time_utc']=today.strftime(format='%Y-%m-%d %H:%M:%S')
        print(my_dict)
        s3 = boto3.client('s3')
        s3.put_object(
             Body=json.dumps(my_dict),
             Bucket='buenbit-fx',
             Key='dt='+today_day+'/time='+today_time+'/'+filename
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

