#!/bin/bash

for f in $(ls transcricoes/*/*/*.mp3);
    do
    # check if the file is already transcribed
    if [ -f ${f%.*}.vtt ]; then
        continue
    fi

    echo "Transcribing $f"    
    whisper $f --model large --language Portuguese --output_dir ${f%/*}
    
    done
