#!/bin/bash

LOGFILE="/home/ubuntu/bitcoin-dashboard/scraper_eth.log"
echo "$(date) : Début de l'exécution du scraper pour l'Ether" >> $LOGFILE

price=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd" \
         | grep -oP '"usd":\K[\d.]+')
echo "$(date) : Prix récupéré = $price" >> $LOGFILE

echo "$(date +'%Y-%m-%d %H:%M:%S'), $price" >> data_eth.csv
echo "$(date) : Fin de l'exécution du scraper pour l'Ether" >> $LOGFILE
