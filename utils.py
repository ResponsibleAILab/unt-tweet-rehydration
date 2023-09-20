import os
import json
from collections import defaultdict

delimiter = '|@|||$|'
input_dir = 'output'
output_dir = 'output_sorted'


# organize date result
def humanreadable_date_result(date_result):
    date = date_result.split(' ')
    week = date[0]
    month = date[1]
    day = date[2]
    time = date[3]
    year = date[5]
    return week, month, day, time, year


# sort extracted csv files
def sort_csv():
    file_list = os.listdir(input_dir)

    for filename in file_list:
        if filename.endswith(".csv"):
            with open(os.path.join(input_dir, filename), 'r') as file:
                lines = file.readlines()

            data = []
            for line in lines:
                elements = line.split(delimiter)
                date = elements[0]
                tid = int(elements[1])
                data.append((date, tid))

            sorted_data = sorted(data, key=lambda x: x[1])

            with open(os.path.join(output_dir, filename), 'ab') as file:
                for date_time, id_value in sorted_data:
                    result = date_time + delimiter + str(id_value) + '\n'
                    result = result.encode('utf-8')
                    file.write(result)


# build dict and create json
def pickle_json():
    result = {}
    temp = defaultdict(list)
    file_list = os.listdir(input_dir)

    for filename in file_list:
        if filename.endswith(".csv"):
            with open(os.path.join(input_dir, filename), 'r') as file:
                lines = file.readlines()

            for line in lines:
                elements = line.split(delimiter)
                date = elements[0]
                tid = int(elements[1])
                _, month, day, time, year = humanreadable_date_result(date)
                # convert month
                month_num = month_to_number.get(month)
                month_str = str(month_num) if month_num >= 10 else '0' + str(month_num)

                ele = time.split(':')
                hour = ele[0]
                minute = ele[1]
                # second = ele[2]
                date_key = year + '-' + month_str + '-' + day + '-' + hour + '-' + minute
                # date_key = year + '-' + month_str + '-' + day + '-' + hour
                # date_key = year + '-' + month_str + '-' + day
                # print(date_key)
                temp[date_key].append(tid)

    # organize result dict
    for day, tid in temp.items():
        min_id = min(tid)
        max_id = max(tid)
        result[day] = {'min': min_id, 'max': max_id}

    # dump to json file
    with open('./json/dict_data_hm.json', 'w') as json_file:
        json.dump(result, json_file)


# find date (search on hour level)
def find_date(id_number):
    # load json file
    with open('./json/dict_data_hm.json', 'r') as file:
        json_data = json.load(file)

    for date, tid in json_data.items():
        if tid['min'] <= id_number <= tid['max']:
            return date
    return None


# month to number
month_to_number = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


# month to number
def month2num(date_result):
    elements = date_result.split('-')
    year = elements[0]
    month = elements[1]
    day = elements[2]
    hour = elements[3]
    minute = elements[4]
    return year, month, day, hour, minute


# if __name__ == '__main__':
#     pickle_json()

