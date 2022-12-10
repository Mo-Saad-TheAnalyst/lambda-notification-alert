import pandas as pd
import awswrangler as wr
import urllib
from mail import send_email


def extract_bucket_name(event):
    name = event["Records"][0]["s3"]["bucket"]["name"]
    return name

def extract_object_key(event):
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    return key 

def read_s3_parquet(bucket,key):
    path = "s3://{AWS_S3_BUCKET}/{key}".format(AWS_S3_BUCKET = bucket,key = key)
    df = wr.s3.read_parquet(path = path)
    return df

def get_stock_header(key):
    header = key.split('/')[-1]
    return header

def get_decrease_percent_message(df:pd.DataFrame,header):
    try:
        min_percent = df['regular_market_change_percent'].min()
    except KeyError:
        pass

    if abs(min_percent) >= 1:
        return "{header} has dropped in price by ".format(header = header ) + str(min_percent)
    else:
        return None

def construct_mail_message(df,header):
    message = None
    notification_list = []
    notification_list.append(get_decrease_percent_message(df,header))
    notification_list = list(filter(None, notification_list))
    message = "\n======================================================================\n".join(notification_list)
    return message


def main(event):
    bucket = extract_bucket_name(event=event)
    key = extract_object_key(event=event)
    header = get_stock_header(key)
    df = read_s3_parquet(bucket,key)
    message = construct_mail_message(df,header)
    if message:
        response = send_email(message=message)
        return response
    else:
        return 'no conditions met'
