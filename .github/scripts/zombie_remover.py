import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def is_link_valid(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        status = response.status_code < 400 or response.status_code == 403
        if "randgallery" in url or "cometa" in url:
            print("Valid: {}".format(url))
        if status:
            print("Valid: {}".format(url))
            return status
        else:
            print("Invalid: {}".format(url))
            return status
    except requests.exceptions.RequestException:
        print("Error: {}".format(url))
        return False

def process_line(args):
    line, archived_file = args
    if not re.match(r'- \[.*?\]\(https?://.*?\) - .*?\.(\s|$)', line):
        return line

    links = re.findall(r'\((https?://.*?)\)', line)
    for link in links:
        if not is_link_valid(link):
            with open(archived_file, 'r') as file:
                archived_content = file.read()
            if line not in archived_content:
                with open(archived_file, 'a') as file:
                    file.write(line)
            return None
    return line

def process_lines(markdown_file, archived_file):
    with open(markdown_file, 'r') as file:
        content = file.readlines()

    with ThreadPoolExecutor() as executor:
        valid_lines = list(executor.map(process_line, [(line, archived_file) for line in content]))

    valid_lines = list(filter(None, valid_lines))

    with open(markdown_file, 'w') as file:
        file.writelines(valid_lines)

def main():
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    markdown_file = os.path.join(project_root, "README.md")
    archived_file = os.path.join(project_root, "ARCHIVED.md")

    process_lines(markdown_file, archived_file)

main()
