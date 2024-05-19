#!/bin/bash

. .venv/bin/activate
python scripts/download.py
./whisper_exec.sh
python scripts/diarization.py
python scripts/union.py
python scripts/fragment_audio.py
python scripts/txt2csv.py
python scripts/csv2json.py
