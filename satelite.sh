cd /var/www/satelite

for CONF in `ls conf/*.conf`; do
  ./functions.sh $CONF
done;