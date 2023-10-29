import boto3
import json

# AWS S3 configuration
hostname = "blr1.vultrobjects.com"
secret_key = "Q60vtZGsZkJ7P7dwfHdJzzNHT3E4RzjeI0dlYEbU"
access_key = "3M5ECKPL2BBJUK7C2IPG"

session = boto3.session.Session()
s3_client = session.client('s3', **{
    "region_name": hostname.split('.')[0],
    "endpoint_url": "https://" + hostname,
    "aws_access_key_id": access_key,
    "aws_secret_access_key": secret_key
})

# Name of your S3 bucket
bucket_name = 'your-new-bucket'

# Assuming the 'bucket_name' already exists

# List objects in the bucket
objects = s3_client.list_objects(Bucket=bucket_name)

# Create a bucket policy to make objects public (if not already done)
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]
}

s3_client.put_bucket_policy(
    Bucket=bucket_name,
    Policy=json.dumps(bucket_policy)
)
print("Bucket made public")

# Path to the video file you want to upload
video_file_path = "video_key.mp4"  # Replace with the actual file path

# Object key (name) for the video in the S3 bucket
video_object_key = "videos/video.mp4"  # Replace with your desired object key

# Upload the video to the S3 bucket
s3_client.upload_file(video_file_path, bucket_name, video_object_key)

print(f"Video '{video_object_key}' uploaded successfully")

# Print the list of video objects in the bucket
print("List of videos in the bucket:")
for obj in objects.get('Contents', []):
    print(obj['Key'])