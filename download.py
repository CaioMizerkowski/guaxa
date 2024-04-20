import urllib.request

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

resp = requests.get("https://www.deviante.com.br/podcasts/rpguaxa/feed/")
soup = BeautifulSoup(resp.text, "xml")
for item in soup.find_all("item"):
    text: str = item.title.text
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
        .lower()
        + ".mp3"
    )
    file = unidecode(file)
    link = item.enclosure.get("url")
    print(file)
    urllib.request.urlretrieve(link, file)
