from utils import date_to_num

# download link
def get_link(date_result):
    base_url = "https://archive.org/download/archiveteam-twitter-stream-"
    year, month, day, _, _ = date_to_num(date_result)
    # print(f"{year} {month} {day}")

    yearmonthday = str(year) + str(month) + str(day)
    year_month_day = str(year) + '_' + str(month) + '_' + str(day)
    yeardmonthdday = str(year) + '-' + str(month) + '-' + str(day)

    twitterdstream = "twitter-stream-"
    twitter_stream = "twitter_stream_"

    if int(year) == 2021:
        if int(month) <= 7:
            url = base_url + str(year) + '-' + str(month) + '/' + twitterdstream + yeardmonthdday + ".zip"
        else:
            url = base_url + str(year) + '-' + str(month) + '/' + twitterdstream + yearmonthday + ".tar"
    elif int(year) == 2020:
        if int(month) <= 6:
            url = base_url + str(year) + '-' + str(month) + '/' + twitter_stream + year_month_day + ".tar"
        else:
            url = base_url + str(year) + '-' + str(month) + '/' + twitterdstream + yeardmonthdday + ".zip"
    elif int(year) == 2019:
        if int(month) <= 7:
            url = base_url + str(year) + '-' + str(month) + '/' + twitter_stream + year_month_day + ".tar"
        elif int(month) == 8 or int(month) == 9:
            url = base_url + str(year) + '-' + '08' + '/' + twitter_stream + year_month_day + ".tar"
        else:
            url = base_url + '2018' + '-' + str(month) + '/' + twitter_stream + year_month_day + ".tar"
    elif int(year) == 2018:
        if int(month) <= 4:
            url = base_url + str(year) + '-' + str(month) + '/archiveteam-twitter-stream-' + str(year) + '-' + str(month) + ".tar"
        elif 4 < int(month) <= 10:
            url = base_url + str(year) + '-' + str(month) + '/' + 'twitter-' + yeardmonthdday + ".tar"
        else:
            url = base_url + str(year) + '-' + str(month) + '/' + twitter_stream + year_month_day + ".tar"
    elif int(year) == 2017:
        if int(month) <= 6:
            url = base_url + str(year) + '-' + str(month) + '/archiveteam-twitter-stream-' + str(year) + '-' + str(month) + ".tar"
        elif 6 < int(month) <= 10:
            url = base_url + str(year) + '-' + str(month) + '/' + twitterdstream + yeardmonthdday + ".tar"
        else:
            url = base_url + str(year) + '-' + '11' + '/' + twitterdstream + yeardmonthdday + ".tar"
    elif 2012 <= int(year) <= 2016:
        url = base_url + str(year) + '-' + str(month) + '/archiveteam-twitter-stream-' + str(year) + '-' + str(month) + ".tar"
    else:
        url = ''
    return url
