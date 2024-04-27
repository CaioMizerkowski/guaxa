import json
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


root = Path("transcricoes/rpguaxa")
for dir in root.iterdir():
    csv_file = dir / "union.csv"
    json_file = dir / "union.json"

    csv2json(csv_file, json_file)
