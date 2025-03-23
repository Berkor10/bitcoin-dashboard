#!/bin/bash

echo "Début de l'exécution du scraper pour l'Ether"

price=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd" \
         | grep -oP '"usd":\K[\d.]+')

echo "$(date +'%Y-%m-%d %H:%M:%S'), $price" >> data_eth.csv

echo "Fin de l'exécution du scraper pour l'Ether"
