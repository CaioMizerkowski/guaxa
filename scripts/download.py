import urllib.request
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from tqdm import tqdm
from unidecode import unidecode


def download(feed, categories=None):
    resp = requests.get(feed, timeout=60)
    soup = BeautifulSoup(resp.text, "xml")

    for item in tqdm(soup.find_all("item")):
        text: str = item.title.text
        text = unidecode(text)
        file = (
            text.replace(" ", "_")
            .replace("#", "")
            .replace(":", "")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace("?", "")
            .replace("!", "")
            .replace("%", "")
            .replace(".", "")
            .replace(";", "")
            .replace("'", "")
            .replace('"', "")
            .replace("/", "")
            .replace("\\", "")
            .replace("...", "")
            .lower()
        )
        file += ".mp3"

        for cat in categories:
            if cat in file:
                file = Path("transcricoes") / Path(cat) / Path(file).stem / file
                break
        else:
            cat = "uncategorized"
            file = Path("transcricoes") / Path(cat) / Path(file).stem / file

        if not file.exists():
            print(f"Downloading {file}")
            file.parent.mkdir(parents=True, exist_ok=True)

            link = item.enclosure.get("url")
            urllib.request.urlretrieve(link, file)


if __name__ == "__main__":

    feed = dotenv_values(".env")["PODCAST_FEED"]
    categories = dotenv_values(".env")["CATEGORIES"].split(",")

    download(feed, categories)
