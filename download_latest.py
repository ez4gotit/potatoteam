import requests
from bs4 import BeautifulSoup
import os

# Constants
URL = "https://getbukkit.org/download/vanilla"
VERSION_FILE = "latest_version.txt"
OUTPUT_DIR = "server"
OUTPUT_FILE = "Server.jar"

def get_latest_version_info():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    version = soup.find("div", {"class": "col-sm-3"}).find("h2").text.strip()
    download_link = soup.find("a", {"class": "btn btn-download"})['href']
    print(version, download_link)
    return version, download_link

def save_new_version(version, download_link):
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Check if the latest version is new
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as file:
            old_version = file.read().strip()
        if old_version == version:
            print("No new version found.")
            return False

    # Download and save new version
    with open(VERSION_FILE, 'w') as file:
        file.write(version)
    response = requests.get(download_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_link = soup.find("div", {"class": "well"}).find("h2").find('a')['href']
    response = requests.get(content_link)
    with open(os.path.join(OUTPUT_DIR, OUTPUT_FILE), "wb") as file:
        file.write(response.content)
    print(f"Downloaded {version}")
    return True

if __name__ == "__main__":
    version, download_link = get_latest_version_info()
    save_new_version(version, download_link)
