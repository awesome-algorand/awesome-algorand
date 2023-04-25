from concurrent.futures import ThreadPoolExecutor
import requests
import os
import re


import os
import zipfile
import requests

import hashlib


def is_content_identical(file_path, content):
    with open(file_path, "rb") as file:
        current_content = file.read()

    current_hash = hashlib.md5(current_content).hexdigest()
    new_hash = hashlib.md5(content).hexdigest()

    return current_hash == new_hash


def find_git_urls(markdown_file):
    with open(markdown_file, "r") as file:
        content = file.read()

    urls = list(set(re.findall(r"https://github\.com/[\w-]+/[\w-]+", content)))
    return urls


def append_message_to_readme(content, repo_name, repo_url):
    message = f"> This resource is auto indexed by AwesomeAlgo, all credits to {repo_name}, for more details refer to {repo_url}\n\n---\n\n"  # noqa: E501
    return message + content


def download_readme(url, download_folder):
    repo_name = url.split("/")[-1]
    raw_url = url.replace("github.com", "raw.githubusercontent.com")

    # Check for main and master branches
    branches = ["main", "master", "develop", "dev"]
    for branch in branches:
        readme_url = f"{raw_url}/{branch}/README.md"
        if "aorumbayev/awesome-algorand" in readme_url.lower():
            return

        response = requests.get(readme_url)
        if response.status_code == 200:
            updated_content = append_message_to_readme(
                response.content.decode(), repo_name, url
            )
            file_path = os.path.join(download_folder, f"{repo_name}.md")

            # Only write the file if the content is different
            if not os.path.exists(file_path) or not is_content_identical(
                file_path, updated_content.encode()
            ):
                with open(file_path, "wb") as file:
                    file.write(updated_content.encode())
                    print(f"Downloaded README.md for {repo_name}")
            else:
                print(f"No changes in README.md for {repo_name}")
            return

        else:
            print(f"Failed to download README.md for {repo_name} in {branch} branch")

    print(f"No valid README.md found for {repo_name}")


def parallel_download_readme(urls, download_folder, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        [executor.submit(download_readme, url, download_folder) for url in urls]


def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))


def has_changes_in_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.exists(file_path) or not is_content_identical(
                file_path, open(file_path, "rb").read()
            ):
                return True
    return False


def split_zip_file(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        file_names = zip_file.namelist()
        middle_index = len(file_names) // 2

        left_zip_path = zip_path.replace(".zip", "_left.zip")
        right_zip_path = zip_path.replace(".zip", "_right.zip")

        with zipfile.ZipFile(left_zip_path, "w", zipfile.ZIP_DEFLATED) as left_zip:
            for file_name in file_names[:middle_index]:
                left_zip.writestr(file_name, zip_file.read(file_name))

        with zipfile.ZipFile(right_zip_path, "w", zipfile.ZIP_DEFLATED) as right_zip:
            for file_name in file_names[middle_index:]:
                right_zip.writestr(file_name, zip_file.read(file_name))

    return left_zip_path, right_zip_path


def upload_to_markprompt(zip_path, token):
    url = "https://api.markprompt.com/v1/train"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/zip"}

    with open(zip_path, "rb") as zip_file:
        response = requests.post(url, headers=headers, data=zip_file)

    if response.status_code == 504:  # Gateway Timeout
        left_zip_path, right_zip_path = split_zip_file(zip_path)
        upload_to_markprompt(left_zip_path, token)
        upload_to_markprompt(right_zip_path, token)
    else:
        return response


def main():
    script_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    markdown_file = os.path.join(project_root, "README.md")
    download_folder = os.path.join(project_root, ".github", "indexed_docs")
    token = os.environ.get("MARKPROMPT_TOKEN")
    zip_path = "data.zip"

    urls = find_git_urls(markdown_file)
    os.makedirs(download_folder, exist_ok=True)
    parallel_download_readme(urls, download_folder)

    if has_changes_in_folder(download_folder):
        zip_folder(download_folder, zip_path)
        response = upload_to_markprompt(zip_path, token)

        if response.status_code == 200:
            print("Successfully uploaded to Markprompt.")
        else:
            print("Error uploading to Markprompt. Status code:", response.status_code)
    else:
        print("No changes detected in the folder. Skipping upload.")


main()
