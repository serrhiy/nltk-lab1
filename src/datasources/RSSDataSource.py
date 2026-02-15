from bs4 import BeautifulSoup
from collections import deque
import feedparser, os, csv, time, re

DEQUE_MAX_LEN = 100


class RSSDataSource:
    fieldnames = ["time", "title", "text"]

    def __init__(self, url: str, filename: str):
        if not os.path.isabs(filename):
            raise Exception("Needed absolute path")

        self.filename = filename
        self.url = url
        self.previous_entries_time: deque[str] = deque(maxlen=DEQUE_MAX_LEN)
        self.entries: list[dict] = []

        if os.path.exists(filename):
            with open(filename, "r") as file:
                reader = csv.DictReader(file, fieldnames=self.fieldnames)
                for article in reader:
                    self.previous_entries_time.append(article["time"])
        else:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def request(self):
        articles = feedparser.parse(self.url)
        for article in articles["entries"]:
            title = article["title"]
            tm = time.strftime("%Y-%m-%d %H:%M:%S", article["published_parsed"])
            texts = []
            for content in article["content"]:
                soup = BeautifulSoup(content["value"], "html.parser")
                text = soup.get_text(" ", strip=True)
                texts.append(re.sub(r"\s+", " ", text))
            self.entries.append({"title": title, "time": tm, "text": " ".join(texts)})

    def write_csv(self):
        new_entries = []
        for entry in self.entries[::-1]:
            if entry["time"] not in self.previous_entries_time:
                new_entries.append(entry)

        with open(self.filename, "a") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerows(new_entries)

        for entry in new_entries:
            self.previous_entries_time.append(entry["time"])
        
        self.entries.clear()
