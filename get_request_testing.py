# import requests
# import re
# from bs4 import BeautifulSoup

# def clean_txt(text):
#     # remove urls
#     text = re.sub(r'http\S+', '', text)
#     # remove non alphanumeric characters
#     text = re.sub(r'[^\w\s]', '', text)
#     # remove repeated white space
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# url = "https://news.ycombinator.com/item?id=38024337"

# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")
# data = soup.get_text()
# e = []
# for line in data.splitlines():
#     if len(line.split()) > 30:
#         e.append(line)
# lines = (line.strip() for line in data.splitlines())
# non_empty_lines = (line for line in lines if len(line.split()) > 1)
# filtered_data = "\n".join(non_empty_lines)
# filtered_data = clean_txt(filtered_data)
# with open("test2.html", "w") as file:
#     file.write(filtered_data)


from info_extraction import Extractor

extractor = Extractor()
url = "https://www.dezeen.com/2023/10/25/pulpatronics-paper-rfid-tags/"
summary = extractor.extract(url)
if not summary:
    print("timeout")
print(extractor.extract(url))
