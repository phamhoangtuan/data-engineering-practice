import boto3
import io
import gzip
from botocore import UNSIGNED
from botocore.client import Config

def main():
    # S3 bucket and initial file key as provided in the README.
    bucket = "commoncrawl"
    key = "crawl-data/CC-MAIN-2025-18/wet.paths.gz"
    
    # Create an S3 client that works without credentials.
    s3 = boto3.client(
        "s3", 
        region_name="us-east-1",
        config=Config(signature_version=UNSIGNED)
    )
    
    # 1. Download the .gz file from S3 into memory
    print("Downloading initial .gz file from S3...")
    response = s3.get_object(Bucket=bucket, Key=key)
    gzipped_data = io.BytesIO(response["Body"].read())
    
    # 2. Extract and open the .gz file in memory to read the first line.
    with gzip.GzipFile(fileobj=gzipped_data, mode="rb") as f:
        first_line = f.readline().decode("utf-8").strip()
        print(f"First file URI from initial file: {first_line}")
        # Clean up the key by removing any leading slashes or whitespace.
        s3_key = first_line.lstrip("/").strip()
        print(f"Downloading file with S3 key: {s3_key}")

    # 3. Download the target file using the extracted S3 key and stream its contents.
    print("Streaming the target file from S3 and printing each line...")
    response_2 = s3.get_object(Bucket=bucket, Key=s3_key)
    with gzip.GzipFile(fileobj=response_2["Body"], mode="rb") as f:
        # For each line, decode and print.
        for line in f:
            print(line.decode("utf-8").strip())

if __name__ == "__main__":
    main()
