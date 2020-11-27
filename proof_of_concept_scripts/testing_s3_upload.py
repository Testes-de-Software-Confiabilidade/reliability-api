import boto3
import matplotlib.pyplot as plt
import io


plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
img_data = io.BytesIO()
plt.savefig(img_data, format='png')
img_data.seek(0)

# Let's use Amazon S3
s3 = boto3.resource(
	's3', 
	aws_access_key_id='', 
	aws_secret_access_key='',
)

bucket = s3.Bucket('reliability-images')

a = bucket.put_object(
	Body=img_data, 
	ContentType='image/png', 
	Key='plt_image.png',
	ACL='public-read'
)

# print(a)
# for k,v in a.__dict__.items():
# 	print(k, v)

