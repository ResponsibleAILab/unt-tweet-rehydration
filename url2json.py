import bz2
import os
import shutil
import tarfile

import requests
import zipfile
from utils import *

# download file with given link
def download_file(url, save_path) -> bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"Downloaded {url} to {save_path}")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
    return False

# unzip file
def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

# untar file
def untar_file(file_path, extract_path):
    with tarfile.open(file_path, 'r') as tar:
        tar.extractall(path=extract_path)

# unbz2 file
def unbz2_file(bz2_file, destination):
    # Open .bz2 file for reading and create output file for writing
    with bz2.open(bz2_file, 'rb') as source_file, open(destination, 'wb') as dest_file:
        dest_file.write(source_file.read())

# return json, zip file
def zip2json(file_path, extract_dest, final_dest):
    unzip_file(file_path, extract_dest)
    post_process(extract_dest, final_dest)

# tar to json
def tar2json(tar_file, extract_dest, final_dest):
    untar_file(tar_file, extract_dest)
    post_process(extract_dest, final_dest)

# post process the files
def post_process(archive, destination):
    # unbz2 file
    unbz2_file(archive, destination)

    # delete
    if os.path.exists(archive):
        if os.path.isdir():
            shutil.rmtree(archive)
        else:
            os.remove(archive)
    else:
        print('Delete fail, path not found')