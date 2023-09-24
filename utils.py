import bz2
import json
import tarfile
import zipfile
import requests
from typing import List

# find date (search on hour level)
def find_dates(ids: List[int]):
    # load json file
    ret_data = []
    with open('./data/dict_data_hm.json', 'r') as file:
        json_data = json.loads(file.read())

    for date in json_data.keys():
        for id in ids:
            min = json_data[date]["min"]
            max = json_data[date]["max"]
            if min <= id <= max:
                ret_data.append((id, date))
                continue
                
    return ret_data

def date_num_to_str(date: int) -> str:
    s = str(date)
    if len(s) == 1:
        return f'0{s}'
    return s

# month to number
def date_to_num(date_result):
    elements = [date_num_to_str(item) for item in date_result.split('-')]
    year = elements[0]
    month = elements[1]
    day = elements[2]
    hour = elements[3]
    minute = elements[4]
    return year, month, day, hour, minute

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

def date_to_file(date: str) -> str:
    _, month, day, hour, minute = date_to_num(date)
    return str(month) + '/' + str(day) + '/' + str(hour) + '/' + str(minute) + '.json.bz2'

# unzip file
def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

# untar file
def untar_file(file_path, extract_path):
    with tarfile.open(file_path, 'r') as tar:
        tar.extractall(path=extract_path)

def get_tweets_from_bz2(bz2_file, ids: List[int]) -> list:
    # Open .bz2 file for reading and create output file for writing
    result = []
    with bz2.open(bz2_file, 'rb') as source_file:
        line = source_file.readline()
        # print(line)
        while line:
            json_element = json.loads(line)
            # print(json_element)
            if 'created_at' in json_element:
                # print("YES!!!")
                for tid in ids:
                    # print(json_element)
                    # print(tid)
                    # print(type(tid))
                    # print(json_element['id'])
                    if tid == json_element['id']:
                        result.append(json_element)
                        break
            line = source_file.readline()
    # print(result)
    return result
