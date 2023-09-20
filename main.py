import os
import sys
import json
from typing import List, Tuple
from utils import find_date, date_to_num, download_file, tar2json, zip2json
from search import get_link

if len(sys.argv) < 2:
    raise Exception('Usage: python main.py [json ids_file]')

file_name = sys.argv[1]
if not os.path.exists(file_name):
    raise Exception(f'Error: file \"{file_name}\" does not exist')

ids = []
with open(file_name, 'r', encoding='utf-8') as f:
    try:
        ids = json.loads(f.read())
    except:
        raise Exception(f"Error: could not parse file \"{file_name}\", is the json formatting correct?")
    if not isinstance(ids, List):
        raise Exception("Error: json file must be a list of ids")

new_ids = []
for id in ids:
    try:
        new_ids.append(int(id))
    except:
        raise Exception(f'Error: Could not convert id {id} to an integer')

ids = new_ids

print(f'Info: found {len(ids)} ids, getting download links')

# turn each id into a tuple (id, date)
tups = []
for id in ids:
    # TODO: this is VERY slow
    tups.append((id, find_date(id)))

def sort_tups(tup: Tuple[int, str]):
    year, month, day, hour, minute = date_to_num(tup[1])
    year = year - 2010
    return minute + hour * 60 + day * 60 * 24 + month * 60 * 24 * 30 + year * 60 * 24 * 365

tups = sorted(tups, key=sort_tups)

group_by_hm = { }
current_date = None
current_ids = []
for id, date in tups:
    if date != current_date:
        if current_date != None:
            group_by_hm[current_date] = current_ids
            current_ids = []
        current_date = date
    current_ids.append(id)

def sort_dates(date: str):
    year, month, day, _, _ = date_to_num(date)
    year = year - 2010
    return day + month * 30 + year * 365

keys = sorted(group_by_hm.keys(), key=sort_dates)

days_to_download = []
current_key = None
for key in group_by_hm.keys():
    new_key = key[:10]
    if new_key != current_key:
        days_to_download.append(new_key)
        current_key = new_key

links = []        
for day in days_to_download:
    ids = []
    for key in group_by_hm.keys():
        day_key = key[:10]
        if day_key == day:
            ids.append({
                "time": key,
                "ids": group_by_hm[key]
            })
    links.append({
        "day": day, 
        "link": get_link(f'{day}-00-00'),
        "ids": ids
    })

print(f'Info: Found {len(links)} days of tweets to download:')
for obj in links:
    day = obj["day"]
    link = obj["link"]
    print(f'\t{day}: {link}')

print('Info: Now Downloading files:')

download_folder = 'downloads'
if not os.path.exists(download_folder):
    os.mkdir(download_folder)


extract_folder = 'extracted_files'
if not os.path.exists(os.mkdir(extract_folder)):
    os.mkdir(extract_folder)

if not os.path.exists(f'{extract_folder}/zip'):
    os.mkdir(f'{extract_folder}/zip')

if not os.path.exists(f'{extract_folder}/tar'):
    os.mkdir(f'{extract_folder}/tar')

for obj in links:
    day = obj["day"]
    extension = obj['link'][-4:]
    download_dest = f'{download_folder}/{extension[-3:]}/{day}{extension}'

    # TODO: Don't skip the day and determine if the archive contents has already been extracted
    if os.path.exists(download_dest):
        print(f'Warning: Found data already at {download_dest} skipping this day...')
        continue
    print(f'Info: Downloading data for {day} to {download_dest}...')
    success = download_file(obj['link'], download_dest)
    # If the download did not succeed, skip this day
    if not success:
        continue
    
    print('Info: Download succeeded, extracting folder')
    extract_dest = f'{extract_folder}/{extension[-3:]}/{day}'
    final_dest = f'{extract_folder}/{day}'

    if extension == '.tar':
        tar2json(download_dest, extract_dest, final_dest)
    
    if extension == '.zip':
        zip2json(download_dest, extract_dest, final_dest)

    print(f'Info: Extraction complete contents extracted to {final_dest}')

    # TODO: Find tweet ids in downloaded files