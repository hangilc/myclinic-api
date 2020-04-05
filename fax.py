from twilio.rest import Client
import os
import sys
import boto3
from pathlib import Path
import time

twilio_sid = os.environ["TWILIO_SID"]
twilio_token = os.environ["TWILIO_TOKEN"]
twilio_phone = os.environ["TWILIO_PHONE"]
client = Client(twilio_sid, twilio_token)
bucket_name = os.environ["MYCLINIC_S3_FAX_BUCKET"]
cloudfront_url = os.environ["MYCLINIC_CLOUDFRONT_FAX_URL"]
cloudfront_user = os.environ["MYCLINIC_CLOUDFRONT_FAX_USER"]
cloudfront_pass = os.environ["MYCLINIC_CLOUDFRONT_FAX_PASS"]


def upload_to_s3(src_file, dst_name):
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).upload_file(src_file, dst_name)


def fetch_fax(fax_sid):
    return client.fax.faxes(fax_sid).fetch()


def send_fax(to_phone, pdf_file):
    fname = Path(pdf_file).name
    upload_to_s3(pdf_file, fname)
    media_url = f"https://{cloudfront_user}:{cloudfront_pass}@{cloudfront_url}/{fname}"
    fax = client.fax.faxes.create(
        from_=twilio_phone,
        to=to_phone,
        media_url=media_url
    )
    sid = fax.sid
    while True:
        time.sleep(10)
        fetched = fetch_fax(sid)
        print(fetched.status)
        if fetched.status == "delivered":
            break


if __name__ == "__main__":
    to = sys.argv[1]
    file = sys.argv[2]
    send_fax(to, file)

