import requests
from bs4 import BeautifulSoup
from summarizer.sbert import SBertSummarizer


class Extractor:
    def __init__(self):
        self.model = SBertSummarizer('paraphrase-MiniLM-L6-v2')

    def extract(self, url):
        # get summary of webpage
        try:
            html = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:
            print("website: ", url, " Timeout")
            return "", -1
        if html.status_code != 200:
            print("website: ", url, " Error: ", html.status_code)
            return "", -1
        soup = BeautifulSoup(html.content, "html.parser")
        filtered_text = self.__filter_txt(soup.get_text(), 30)
        return self.__generate_summary(filtered_text), self.__word_count("pulpatronics", soup.get_text())

    def __filter_txt(self, text, l):
        # remove any line with length smaller than l
        new_txt = []
        for line in text.splitlines():
            if len(line.split()) >= l:
                new_txt.append(line)
        return "\n".join(new_txt)

    def __generate_summary(self, text, n=3):
        # shorten the text to n number of sentences
        summary = self.model(text, num_sentences=n)
        # remove newlines
        return " ".join(summary.splitlines())
    
    def __word_count(self, keyword, text):
        if not text:
            return -1
        return text.lower().count(keyword.lower())
        
        
