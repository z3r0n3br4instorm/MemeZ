import requests
from bs4 import BeautifulSoup
import random

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
            print(f"Failed to fetch data from Reddit. Status Code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", class_="thing")

        if not posts:
            print("No posts found.")
            return None

        image_posts = []
        for post in posts:
            title_tag = post.find("a", class_="title")
            if title_tag:
                meme_url = title_tag.get("href")
                if meme_url and "i.redd.it" in meme_url:
                    image_posts.append(meme_url)

        if not image_posts:
            print("No image posts found.")
            return None

        # Randomly select a post
        self.memes = random.choice(image_posts)
        return self.memes

    def getMeme(self):
        return self.memes


if __name__ == "__main__":
    redditEngine = RedditEngine()
    meme = redditEngine.fetch("memes")
    if meme:
        print(f"Random Meme URL: {meme}")
    else:
        print("No meme could be fetched.")
