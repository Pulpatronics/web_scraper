import requests
import csv
import sys
import math
from info_extraction import Extractor
from google_drive_sync import GoogleDriveSync
from datetime import datetime

api_key = "AIzaSyAJ9Pqcv2ogk9Zz3rZhLv69uH0mI15QBA4"
search_engine_id = "c41ac0548f58c4e56"
main_keyword = "pulpatronics"
websites_to_exclude = ["pulpatronics", "facebook", "instagram", "twitter", "youtube", "linkedin"]

base_url = "https://www.googleapis.com/customsearch/v1?"
default_params = f"key={api_key}&exactTerms={main_keyword}&cx={search_engine_id}&lr=lang_en&sort=date:d:s"

extractor = Extractor()

domain_names = ["com", "org", "net", "edu", "gov", "int", "mil", "co", "uk", "ca", "de", "jp", "fr", "au", "us", "ru", "ch", "it", "nl", "se", "no", "es", "mil", "io", "ai", "ly", "gl"]

def request_builder(dateRestrict=None, excludeTerm=None, start=1, orTerms=None, excludeWebsites=None):
    """
    dateRestrict: results from specfic number of past days,
    excludeTerm: 1 term to exclude from search
    start: start index of search
    orTerms: search for one of the terms
    excludeWebsites: websites to exclude from search
    """
    params = default_params
    params += f"&start={start}"
    if dateRestrict:
        params += f"&dateRestrict={dateRestrict}"
    if excludeTerm:
        params += f"&excludeTerms={excludeTerm}"
    if orTerms:
        params += f"&orTerms={orTerms}"
    if excludeWebsites:
        params += f"&excludeSites={excludeWebsites}"
    return params


def result_parser(result, date):
    """
    result: json object
    """
    data = []
    print(result.keys())
    for item in result["items"]:
        title = item["title"]
        # if "article" not in item["pagemap"]:
        #     continue
        if "metatags" not in item["pagemap"]:
            continue
        display_link = item["displayLink"].split("/")[0]
        if any(name in display_link for name in websites_to_exclude):
            continue
        parts = display_link.split(".")
        # remove domain names and www
        publisher = []
        for part in parts:
            if "www" not in part and part not in domain_names:
                publisher.append(part)
        publisher = ".".join(publisher)
        date = None
        if "article:published_time" in item["pagemap"]["metatags"][0]:
            date = item["pagemap"]["metatags"][0]["article:published_time"].split("T")[0]
        if  "article:modified_time" in item["pagemap"]["metatags"][0]:
            date = item["pagemap"]["metatags"][0]["article:modified_time"].split("T")[0]
        link = item["link"]
        summary, word_count = extractor.extract(link)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        data.append({"Timestamp": timestamp, "Title": title, "Date": date, "Publisher": publisher, "Link": link, "MentionCount": word_count, "Summary": summary})
    return data

# timestamp: when the data is collected
# title: title of the website
# date: date of the article, if available
# publisher: base url of the website
# link: full url of the website
# summary: 5 sentence summary of the website
fieldnames = ["Timestamp", "Title", "MentionCount", "Date", "Publisher", "Link", "Summary"]

def save_to_csv(data, filename="test.csv"):
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def __main__():
    args = sys.argv
    n = 10
    if len(args) > 1:
        n = math.ceil(int(args[1]) / 50)
    start = 1
    data = []
    date = datetime.now().strftime("%Y-%m-%d")
    for _ in range(n):
        params = request_builder(start=start, dateRestrict=200)
        result = requests.get(base_url + params)
        if result.status_code != 200:
            print(f"Error: {result.status_code}")
            print()
        else:
            # print(result.text)
            if "items" not in result.json():
                print("No items found in :", result.json())
                break
            data += result_parser(result.json(), date)
        start += 10
    save_to_csv(data)
    sync = GoogleDriveSync()
    sync.update_file("test.csv", "test.csv")
    

if __name__ == "__main__":
    __main__()
