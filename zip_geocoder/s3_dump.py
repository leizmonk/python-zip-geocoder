"""Take source JSON file and dump to S3 bucket."""

import boto
import boto.s3
import sys
from boto.s3.key import Key

with open('../.env') as file:
    content = file.readlines()
    parsed = [x.strip().split('=') for x in content]
    config = dict(parsed)

AWS_ACCESS_KEY_ID = config.get('AWS_IAM_KEY')
AWS_SECRET_ACCESS_KEY = config.get('AWS_IAM_SECRET')

bucket_name = 'wx-aggregator'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

bucket = conn.lookup(bucket_name)

uplaod_file = 'zipcodes.json'
print 'Uploading %s to Amazon S3 bucket %s' % \
    (uplaod_file, bucket_name)


def percent_cb(complete, total):
    """Write to S3."""
    sys.stdout.write('.')
    sys.stdout.flush()

k = Key(bucket)
k.key = 'zipcodes.json'
k.set_contents_from_filename(uplaod_file, cb=percent_cb, num_cb=10)
