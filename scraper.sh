#!/bin/bash

# Chemin absolu pour le log
LOGFILE="/home/ubuntu/bitcoin-dashboard/scraper.log"

echo "$(date) : Début de l'exécution du scraper" >> $LOGFILE

# Appel à l’API CoinGecko pour récupérer le prix du Bitcoin en USD
# Utilisation d'un chemin absolu pour curl et grep (les chemins habituels sous Ubuntu)
price=$(/usr/bin/curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd" \
       | /usr/bin/grep -oP '"usd":\K[\d.]+')

echo "$(date) : Prix récupéré = $price" >> $LOGFILE

# Écriture des données dans data.csv (avec chemin absolu)
echo "$(date +'%Y-%m-%d %H:%M:%S'), $price" >> /home/ubuntu/bitcoin-dashboard/data.csv

echo "$(date) : Fin de l'exécution du scraper" >> $LOGFILE

