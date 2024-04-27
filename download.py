import urllib.request
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

resp = requests.get("https://www.deviante.com.br/podcasts/rpguaxa/feed/", timeout=60)
soup = BeautifulSoup(resp.text, "xml")
for item in soup.find_all("item"):
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

    if "guaxaverso" in file:
        file = Path("transcricoes/guaxaverso/") / Path(file).stem / file
    elif "rpguaxa" in file:
        file = Path("transcricoes/rpguaxa/") / Path(file).stem / file
    else:
        print("Not a valid podcast:", file)
        continue

    if not file.exists():
        print(file)
        file.parent.mkdir(parents=True, exist_ok=True)

        link = item.enclosure.get("url")
        urllib.request.urlretrieve(link, file)
