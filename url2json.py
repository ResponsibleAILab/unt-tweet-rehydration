import bz2
import os
import shutil
import tarfile

import requests
import zipfile
from utils import *


# download file with given link
def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print(f"Downloaded {url} to {save_path}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")


# unzip file
def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


# untar file
def untar_file(file_path, extract_path):
    with tarfile.open(file_path, 'r') as tar:
        tar.extractall(path=extract_path)


# unbz2 file
def unbz2_file(file_name):
    # Open .bz2 file for reading and create output file for writing
    output_filepath = os.path.splitext(file_name)[0]  # Remove .bz2 extension
    with bz2.open(file_name, 'rb') as source_file, open(output_filepath, 'wb') as dest_file:
        dest_file.write(source_file.read())
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print('Delete fail, file not found')
    except Exception as e:
        print(f"An error occurred: {e}")


# return json, zip file
def zip2json(download_link, file_path):
    file_name = download_link.split("/")[-1]
    save_path = file_name

    # download_file(download_link, save_path)
    unzip_file(file_name, './')

    # post_process(file_path, file_name)


# tar to json
def tar2json(download_link, file_path):
    file_name = download_link.split("/")[-1]
    save_path = file_name

    download_file(download_link, save_path)
    untar_file(file_name, './')

    # post_process(file_path, file_name)


# post process the files
def post_process(file_path, file_name):
    # move
    des_path = './' + file_path.split('/')[-1]
    try:
        shutil.move(file_path, des_path)
    except Exception as e:
        print(f"Error moving the file: {e}")

    # unbz2 file
    unbz2_file(des_path)

    # delete
    dir_name = file_path.split('/')[1]
    try:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        else:
            print('Delete fail, path not found')

        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print('Delete fail, file not found')
    except Exception as e:
        print(f"An error occurred: {e}")


# binary search
def binary_search(csv_data, target_id):
    left, right = 0, len(csv_data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_id = csv_data[mid]['id']

        if mid_id == target_id:
            return csv_data[mid]['date']
        elif mid_id < target_id:
            left = mid + 1
        else:
            right = mid - 1

    return None


if __name__ == "__main__":
    # id_number = 1296904746960408577
    # download_link = "https://archive.org/download/archiveteam-twitter-stream-2020-08/twitter-stream-2020-08-21.zip"
    id_number = 823004070155866112
    download_link = "https://archive.org/download/archiveteam-twitter-stream-2017-01/archiveteam-twitter-stream-2017-01.tar"
    # id_number = 1136609521067913217
    # download_link = "https://archive.org/download/archiveteam-twitter-stream-2019-06/twitter_stream_2019_06_06.tar"
    delimiter = '|@|||$|'

    date_info = find_date(id_number)
    year, month, day, hour, minute = month2num(date_info)

    if download_link[-4:] == '.zip':
        file_path = './' + str(year) + '/' + str(month) + '/' + str(day) + '/' + str(hour) + '/' + str(minute) + '.json.bz2'
        zip2json(download_link, file_path)
    elif download_link[-4:] == '.tar':
        file_path = './' + str(month) + '/' + str(day) + '/' + str(minute) + '.json.bz2'
        tar2json(download_link, file_path)