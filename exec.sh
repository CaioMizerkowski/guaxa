for f in *.mp3; do echo $f; whisper $f --model large --language Portuguese ; done

for f in *.vtt; do nf=${f%.*}; mkdir -p ${nf}; mv ${nf}.* ${nf}/ ; done

mkdir transcricoes
mkdir transcricoes/rpguaxa
mkdir transcricoes/guaxaverso
mv *rpguaxa* transcricoes/rpguaxa/
mv *guaxaverso* transcricoes/guaxaverso/
