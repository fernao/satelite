#!/bin/bash

# gerar novas entradas json para timeline


echo ',' >> $DATA_JSON
echo '       {' >> $DATA_JSON
echo '            "title": "'$NAME-$NOW'",' >> $DATA_JSON
echo '            "id":    "'$IMAGEM'",' >> $DATA_JSON
echo '            "start": "'$NOW_JSON'",' >> $DATA_JSON
echo '            "icon":  "'IMAGES_FOLDER=$BASE_FOLDER/imagens/$NAME/$IMAGEM'"' >> $DATA_JSON
echo '       }' >> $DATA_JSON