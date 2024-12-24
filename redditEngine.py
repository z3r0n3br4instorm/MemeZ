import requests
from bs4 import BeautifulSoup
import os


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}


class RedditEngine:
    def __init__(self):
        self.memes = None

    def fetch(self, subredditName):
        URL = f"https://old.reddit.com/r/{subredditName}/"
        response = requests.get(URL, headers=HEADERS)
        if response.status_code != 200:
            print(
                f"Failed to fetch data from Reddit. Status Code: {response.status_code}"
            )
            return
        soup = BeautifulSoup(response.text, "html.parser")
        latest_post = soup.find("div", class_="thing")

        if not latest_post:
            print("No memes found.")
            return

        title_tag = latest_post.find("a", class_="title")
        if title_tag:
            meme_url = title_tag.get("href")
            if "i.redd.it" in meme_url:
                self.memes = meme_url
                return self.memes
            else:
                print("The latest post is not a direct image.")
                return None
        else:
            print("No valid post found.")
            return None

    def getMeme(self):
        return self.memes
