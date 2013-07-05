#!/bin/bash
#
# TODO: mkdir auto
# TODO: mensagens de erro no log

# confs
BASE_FOLDER=`pwd`
LOG_FOLDER=$BASE_FOLDER/'logs'
NOW=`date +%Y_%m_%d_%H.%M`
NOW_JSON=`date +%Y-%m-%d-%H-%m`
IMAGEM=$NOW.jpg
DEFAULT_THUMB_SIZE=x150
DATA_JSON=$BASE_FOLDER/data.json
HASH=md5sum

# inicializa instancia 
source $1
IMAGES_FOLDER=$BASE_FOLDER/imagens/$NAME
IMAGEM_THUMB_FOLDER=$IMAGES_FOLDER/thumb
IMAGEM_THUMB=$IMAGES_THUMB_FOLDER/$NAME

echo "=============================================================="
echo "PASTA:    $NAME"  / $IMAGES_FOLDER
echo "=============================================================="

# verifica imagem anterior
if [ -d $IMAGES_FOLDER ]; then 
  echo 1 > /dev/null
else 
  mkdir -p $IMAGES_FOLDER
fi

cd $IMAGES_FOLDER

LAST_IMG=`cat $IMAGES_FOLDER/LAST_IMG`
echo $LAST_IMG

cp $LAST_IMG imagem.jpg
HASH_LAST=`$HASH imagem.jpg`

# baixa arquivo como imagem
wget -nv -S $SRC -O imagem.jpg
# faz checagem de hash da ultima imagem
HASH_NOW=`$HASH imagem.jpg`

# se verboso
# echo $HASH_LAST
# echo $HASH_NOW

if [ "$HASH_LAST" == "$HASH_NOW" ]; then
  echo "IMAGEM IGUAL - NAO SERA GRAVADO"
  rm imagem.jpg
else 
  echo "GRAVANDO NOVA IMAGEM"
  mv imagem.jpg $IMAGEM
  
  # ##
  # gera thumbnail
  if [ -n "${THUMB_SIZE}" ]; then 
      SIZE=$THUMB_SIZE
  else
      SIZE=$DEFAULT_THUMB_SIZE
  fi
#  convert -geometry $SIZE $IMAGEM $IMAGEM_THUMB
  
  # cria entrada json
#  source $BASE_FOLDER/gera_json.sh
  
  # finaliza e grava log
  echo $IMAGEM > LAST_IMG
  echo "`date +%H:%M\ %Y\ %m\ %d` -  nova imagem gravada." >> $LOG_FOLDER/$NAME.log
fi