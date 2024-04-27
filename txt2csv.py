from itertools import chain
from pathlib import Path


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


root1 = Path("transcricoes/guaxaverso")
root2 = Path("transcricoes/rpguaxa")
chain_root = chain(root1.iterdir(), root2.iterdir())

for dir in sorted(chain_root):
    csv_file = dir / "union.csv"
    txt_file = dir / "union.txt"

    txt2csv(txt_file, csv_file)
