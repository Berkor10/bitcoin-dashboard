#!/bin/bash
# Récupération du contenu HTML de la page
html=$(curl -s "https://www.coingecko.com/en/coins/bitcoin")

# Extraction du prix du Bitcoin via une regex adaptée à la structure HTML (à adapter si nécessaire)
price=$(echo "$html" | grep -oP 'data-target="price.price".*?[\d,.]+' | grep -oP '[\d,.]+')

# Sauvegarde des données avec timestamp dans data.csv
echo "$(date +'%Y-%m-%d %H:%M:%S'), $price" >> data.csv
