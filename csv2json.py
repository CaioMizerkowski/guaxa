import json
from itertools import chain
from pathlib import Path

fields = ["id", "start", "end", "speakers", "text"]


def csv2json(csv_file, json_file):
    with open(csv_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    data = []
    for idx, line in enumerate(lines):
        line = line.split(";")
        line = [idx] + line
        data.append(dict(zip(fields, line)))

    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)


root1 = Path("transcricoes/guaxaverso")
root2 = Path("transcricoes/rpguaxa")
chain_root = chain(root1.iterdir(), root2.iterdir())


for dir in sorted(chain_root):
    csv_file = dir / "union.csv"
    json_file = dir / "union.json"

    csv2json(csv_file, json_file)
