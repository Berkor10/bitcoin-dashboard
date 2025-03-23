#!/bin/bash
# Chemin pour le fichier log
LOGFILE="/home/ubuntu/bitcoin-dashboard/scraper_eth.log"

echo "$(date +'%Y-%m-%d %H:%M:%S') : Début de l'exécution du scraper pour l'Ether" >> $LOGFILE

# Récupération du prix via l'API CoinGecko
price=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd" | grep -oP '"usd":\K[\d.]+')
echo "$(date +'%Y-%m-%d %H:%M:%S') : Prix récupéré = $price" >> $LOGFILE

# Écriture dans le fichier CSV avec chemin absolu
echo "$(date +'%Y-%m-%d %H:%M:%S'), $price" >> /home/ubuntu/bitcoin-dashboard/data_eth.csv

echo "$(date +'%Y-%m-%d %H:%M:%S') : Fin de l'exécution du scraper pour l'Ether" >> $LOGFILE
