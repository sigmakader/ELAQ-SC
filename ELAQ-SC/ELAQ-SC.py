import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

print("--------------------------------------------------")
print("         ----- A SMALL PROJECT BY ELAQ -----")
print("--------------------------------------------------\n")

# Ask for URL
url = input("Enter the URL of the site: ").strip()

# Ask what to save
print("\nChoose an option:")
print("1. Save HTML only")
print("2. Save HTML + JS + CSS")
choice = input("Option: ").strip()

# Folder to store downloaded files
folder = "site_data"
os.makedirs(folder, exist_ok=True)

print("\nFetching site data...")

# Get HTML
try:
    r = requests.get(url)
    r.raise_for_status()
except Exception as e:
    print(f"Failed to fetch URL: {e}")
    exit()

html_path = os.path.join(folder, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(r.text)

print("HTML saved.")

if choice == "2":
    soup = BeautifulSoup(r.text, "html.parser")

    def download_file(file_url, subfolder):
        file_name = os.path.basename(urlparse(file_url).path)
        if not file_name:
            return
        file_path = os.path.join(folder, subfolder, file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            file_data = requests.get(file_url).content
            with open(file_path, "wb") as f:
                f.write(file_data)
            print(f"Downloaded: {file_url}")
        except Exception as e:
            print(f"Failed to download {file_url}: {e}")

    # Download CSS files
    for link in soup.find_all("link", {"rel": "stylesheet"}):
        href = link.get("href")
        if href:
            file_url = urljoin(url, href)
            download_file(file_url, "css")

    # Download JS files
    for script in soup.find_all("script", {"src": True}):
        src = script.get("src")
        if src:
            file_url = urljoin(url, src)
            download_file(file_url, "js")

    print("\nAll assets saved in 'site_data' folder.")

print("\nDone! A SMALL PROJECT BY ELAQ")
