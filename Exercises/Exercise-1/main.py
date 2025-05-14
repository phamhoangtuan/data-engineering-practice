import requests
from pathlib import Path
import zipfile
import os

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def create_downloads_dir():
    """Create downloads directory if it doesn't exist"""
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    return downloads_dir


def download_file(url, download_path):
    """Download a file from URL to specified path"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(download_path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.exceptions.RequestException:
        print(f"Failed to download {url}")
        return False
    

def extract_zip(zip_path, extract_dir):
    """Extract ZIP file and delete it afterwards"""
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(extract_dir)
        os.remove(zip_path)
        return True
    except zipfile.BadZipFile:
        print(f"Failed to extract {zip_path}")
        return False


def get_filename_from_url(url):
    """Extract filename from URL"""
    return url.split('/')[-1]


def main():
    # your code here
    downloads_dir = create_downloads_dir()

    for url in download_uris:
        filename = get_filename_from_url(url)
        download_path = downloads_dir / filename

        if download_file(url, download_path):
            extract_zip(download_path, downloads_dir)


if __name__ == "__main__":
    main()
