import boto3

mymail = {
            "ToAddresses": [
                "moh2041999@hotmail.com",
            ],
        }

def send_email(message,receivers = mymail):
    ses_client = boto3.client("ses",region_name = "us-east-1")
    CHARSET = "UTF-8"
    try:
        mail_response = ses_client.send_email(
            Destination = receivers,
            Message={
                "Body": {
                    "Text": {
                        "Charset": CHARSET,
                        "Data": message,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": "Stocks-Notifications",
                },
            },
            Source="moh2041999@hotmail.com",
        )
        print(mail_response)
    except:
        return 'No internet but the message is :' + message
    else:
        return mail_response