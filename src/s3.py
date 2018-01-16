import boto3

s3 = boto3.resource('s3')

lp_bucket = s3.Bucket('license-plate-images')

for item in lp_bucket.objects.all():
    print(item)
