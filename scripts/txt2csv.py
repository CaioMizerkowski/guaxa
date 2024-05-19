from itertools import chain
from pathlib import Path

from dotenv import dotenv_values


def txt2csv(txt_file, csv_file):
    with open(txt_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    data = []
    for line in lines:
        indexes, speakers = line.strip().split("(")
        speakers, text = speakers.split(")")

        indexes = indexes.strip().replace(" ", ";")
        speakers = f'"{speakers.strip()}"'
        text = text.strip()

        new_line = f"{indexes};{speakers};{text}"
        data.append(new_line)

    with open(csv_file, "w") as f:
        for line in data:
            f.write(line + "\n")


if __name__ == "__main__":
    categories = dotenv_values(".env")["CATEGORIES"].split(",")
    iterdirs = [(Path("transcricoes") / cat).iterdir() for cat in categories]

    chain_root = chain(*iterdirs)

    for folder in sorted(chain_root):
        csv_file = folder / "union.csv"
        txt_file = folder / "union.txt"

        txt2csv(txt_file, csv_file)
