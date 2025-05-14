import requests
import pandas as pd
from bs4 import BeautifulSoup


def main():
    # your code here
    base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    target_timestamp = "2024-01-19 10:27"
    
    # 1. Fetch the NOAA data directory HTML
    print("Fetching the NOAA data directory HTML...")
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to fetch HTML page. Status code: {response.status_code}")
        return
    html_content = response.text

    # 2. Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # 3. Search for the file with the matching Last Modified timestamp
    target_file = None
    # The HTML structure may vary; here we try to find elements that contain the target timestamp.
    for element in soup.find_all(text=True):
        if target_timestamp in element:
            parent = element.parent
            # Assume that the file name is in a previous anchor tag in the same row
            a_tag = parent.find_previous("a")
            if a_tag and a_tag.get("href"):
                target_file = a_tag.get("href").strip()
                break

    if not target_file:
        print("Target file with the specified timestamp not found.")
        return
    
    print(f"Found target file: {target_file}")

    # 4. Download the file
    file_url = base_url + target_file
    print(f"Downloading file from {file_url}...")
    file_response = requests.get(file_url)
    if file_response.status_code != 200:
        print(f"Failed to download file. Status code: {file_response.status_code}")
        return
    
    local_filename = target_file  # Save with the original file name
    with open(local_filename, "wb") as f:
        f.write(file_response.content)
    print(f"File downloaded and saved as {local_filename}.")
    
    # 5. Load the file into a Pandas DataFrame
    print("Loading file into Pandas DataFrame...")
    try:
        df = pd.read_csv(local_filename)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # 6. Find record(s) with the highest HourlyDryBulbTemperature
    if "HourlyDryBulbTemperature" not in df.columns:
        print("Column 'HourlyDryBulbTemperature' not found in the data.")
        return
    
    max_temp = df["HourlyDryBulbTemperature"].max()
    records = df[df["HourlyDryBulbTemperature"] == max_temp]
    
    print("Record(s) with the highest HourlyDryBulbTemperature:")
    print(records)
    


if __name__ == "__main__":
    main()
