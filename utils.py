import json

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
def date_to_num(date_result):
    elements = date_result.split('-')
    year = elements[0]
    month = elements[1]
    day = elements[2]
    hour = elements[3]
    minute = elements[4]
    return year, month, day, hour, minute


# if __name__ == '__main__':
#     pickle_json()

