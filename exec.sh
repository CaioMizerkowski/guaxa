#!/bin/bash

. .venv/bin/activate
python scripts/download.py

for f in $(ls transcricoes/*/*/*.mp3);
    do
    # check if the file is already transcribed
    if [ -f ${f%.*}.vtt ]; then
        continue
    fi

    echo "Transcribing $f"    
    whisper $f --model large --language Portuguese --output_dir ${f%/*}
    
    done

python scripts/diarization.py
python scripts/union.py
python scripts/fragment_audio.py
python scripts/txt2csv.py
python scripts/csv2json.py
