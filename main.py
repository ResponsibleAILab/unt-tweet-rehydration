import os
import sys
import json
import shutil
from typing import List, Tuple, Dict

from link import get_link
from utils import find_dates, date_to_num, download_file, untar_file, date_to_file, get_tweets_from_bz2, unzip_file

# Check arguments
# if len(sys.argv) < 3:
#     raise Exception('Usage: python main.py [json ids_file] [json output_file]')

# # Check if output file already exists
# output_file = sys.argv[2]
# if os.path.exists(output_file):
#     raise Exception(f'Error: file \"{output_file}\" already exists')

# # Check if id file exists
# ids_file = sys.argv[1]
# if not os.path.exists(ids_file):
#     raise Exception(f'Error: file \"{ids_file}\" does not exist')


# test input: {"twitter_ids":["1267433197312389123", "1410539511088484357"]}
# {"twitter_ids":["1275688887810211844"]}


ids_file = 'ids.json'
output_file = 'tweets.json'

# Validate ids file
ids = []
with open(ids_file, 'r', encoding='utf-8') as f:
    try:
        ids = json.loads(f.read())
    except:
        raise Exception(f"Error: could not parse file \"{ids_file}\", is the json formatting correct?")
    if not isinstance(ids, List) and not isinstance(ids, Dict) or isinstance(ids, Dict) and 'twitter_ids' not in ids:
        raise Exception("Error: json file must be a list of ids or an object with a list of ids with the key \"twitter_ids\"")
    
    if isinstance(ids, Dict):
        ids = ids["twitter_ids"]

# Parse ids into integers
new_ids = []
for id in ids:
    try:
        new_ids.append(int(id))
    except:
        raise Exception(f'Error: Could not convert id {id} to an integer')

# Check for empty list
ids = new_ids
if len(ids) == 0:
    raise Exception('Error: Found 0 ids, exiting')

print(f'Info: {len(ids)} tweet ids in input file, finding date information for ids')

# Find date information for ids
tups = find_dates(ids)

print(f'Info: found {len(tups)} of {len(ids)} input id dates ({len(tups) / len(ids) * 100:.0f}%)')

if len(tups) == 0:
    raise Exception('Error: Found 0 dates for ids, exiting')

print(f'Info: found {len(ids)} ids, getting download links')

def sort_tups(tup: Tuple[int, str]):
    year, month, day, hour, minute = date_to_num(tup[1])
    year = int(year) - 2010
    return int(minute) +int(hour) * 60 + int(day) * 60 * 24 + int(month) * 60 * 24 * 30 + int(year) * 60 * 24 * 365

# Sort by date
tups = sorted(tups, key=sort_tups)
# print(tups)

# Group ids by date
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

group_by_hm[current_date] = current_ids

def sort_dates(date: str):
    year, month, day, _, _ = date_to_num(date)
    year = int(year) - 2010
    return int(day) + int(month) * 30 + year * 365

# Sort grouped dates
keys = sorted(group_by_hm.keys(), key=sort_dates)

# Get days to download
days_to_download = []
current_key = None
for key in group_by_hm.keys():
    new_key = key[:10]
    if new_key != current_key:
        days_to_download.append(new_key)
        current_key = new_key

# Aggregate data into one object
links = []
for day in days_to_download:
    ids = []
    for key in group_by_hm.keys():
        day_key = key[:10]
        if day_key == day:
            extension = get_link(f'{day}-00-00')[-4:]
            ids.append({
                "time": key,
                "ids": group_by_hm[key],
                "file": date_to_file(key, extension)
            })
    links.append({
        "day": day, 
        "link": get_link(f'{day}-00-00'),
        "ids": ids
    })

# Show user the files that will be downloaded
print(f'Info: Found {len(links)} days of tweets to download:')
for obj in links:
    day = obj["day"]
    link = obj["link"]
    print(f'\t{day}: {link}')

print('Info: Now Downloading files:')

# Create downloads folder if needed
download_folder = 'downloads'
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

# Create extraction folder if needed
extract_folder = 'extracted_files'
if not os.path.exists(extract_folder):
    os.mkdir(extract_folder)

# Download links one at a time
num_found_tweets = 0
for obj in links:
    day = obj["day"]
    extension = obj['link'][-4:]
    download_dest = f'{download_folder}/{day}{extension}'

    # Don't download file if found already
    if os.path.exists(download_dest):
        print(f'Warning: Found data already at \"{download_dest}\" moving to extraction phase')
    else:
        print(f'Info: Downloading data for {day} to {download_dest}...')
        link = obj['link']
        success = download_file(link, download_dest)
        if success:
            print('Info: Download succeeded, extracting folder')
        else:
            print(f'Warning: Download failed for \"{link}\", going to next link')
            continue
    
    extract_dest = f'{extract_folder}/{day}'

    # Delete extraction folder if it already exists
    if os.path.exists(extract_dest):
        shutil.rmtree(extract_dest)

    all_tweets = []
    if extension == '.tar':
        untar_file(download_dest, extract_dest)
    
    if extension == '.zip':
        unzip_file(download_dest, extract_dest)

    print('Info: Extraction complete')

    # For each group of ids (by hour/minute)  find the bz2 file, extract the json, and then find the tweets needed
    for id_obj in obj["ids"]:
        for path, _, bz_files in os.walk(extract_dest):
            for bz_file in bz_files:
                file = path + '/' + bz_file
                for tweet in get_tweets_from_bz2(file, id_obj["ids"]):
                    all_tweets.append(tweet)


    # Clean up extraction data
    shutil.rmtree(extract_dest)

    # Find ids currently in file, this allows for stopping and starting downloads at a later time
    if os.path.exists(output_file):
        current_ids = []
        with open(output_file, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                data = json.loads(line)
                current_ids.append(data["id"])
                line = f.readline()

    # Write output file
    with open(output_file, 'a', encoding='utf-8') as f:
        for tweet in all_tweets:
            if tweet["id"] not in current_ids:
                f.write(json.dumps(tweet) + '\n')
    
    print(f'Info: wrote {len(all_tweets)} tweets to {output_file}')
    num_found_tweets += len(all_tweets)

# Delete extraction folder that is not needed, downloads folder is kept for backups
shutil.rmtree(extract_folder)

# Delete downloaded zip or tar data (Do it in final edition)
# shutil.rmtree(download_folder)

print(f'Info: Done processing files, found {num_found_tweets} out of {len(ids)} ({num_found_tweets / len(ids) * 100:.0f}%)')