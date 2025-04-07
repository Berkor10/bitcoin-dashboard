# 📈 Bitcoin & Ethereum Dashboard

## 📌 Overview

Managing crypto price tracking manually is tedious and error-prone. BTC-ETH Dashboard solves this by offering an automated system that scrapes and collects crypto prices, stores them, and displays everything in a modern, interactive dashboard using Dash.
You get real-time prices, a BTC→USD converter, volatility analysis, and even daily reports—all automatically updated via cron jobs.
ps: We made the commits from the VM, so they're marked “Ubuntu” on github, but they were made by both of us.

## 👨‍💻 Meet the Use Case

Imagine you’re a crypto enthusiast who wants to monitor Bitcoin and Ethereum prices over time, understand volatility, and visualize trends—all without having to code or check multiple platforms manually. With BTC-ETH Dashboard, you get:
✅ Real-time Bitcoin price updates
✅ Ethereum price tracking via API
✅ Automatic daily reports (min, max, returns, volatility)
✅ BTC/USD converter
✅ Volatility graph with rolling windows


---

## 🔥 Features

✅ Scraping & API – Bitcoin data via Bash & regex; Ether via CoinGecko API
✅ Cron Automation – Data refreshed every 5 minutes, reports generated daily
✅ Real-Time Price Display – Live BTC price updated every 60s in the dashboard
✅ Converter BTC → USD – Simple input for fast conversion
✅ MA5 Graphs – Visualize BTC with moving averages
✅ Dual-Axis Chart – Compare BTC & ETH trends with one clean graph
✅ Rolling Volatility – Track BTC’s changing risk profile over time
✅ Daily Report – Auto-generated insights saved in a file and read by the dashboard

---

## 📊 How It Works

1️⃣ scraper.sh runs every 5 min to scrape BTC price from CoinGecko → data.csv
2️⃣ scraper_eth.sh fetches ETH/USD via CoinGecko API → data_eth.csv
3️⃣ Dashboard reads these CSV files and displays price graphs + indicators
4️⃣ At midnight, daily_report.py runs via cron and writes a summary into daily_report.txt
5️⃣ The Dash app loads this report + all graphs in a stylish web interface

---

## 🔧 Technical Details
	•	Scraping: Bash, curl, regex
	•	API: CoinGecko REST API
	•	Scheduling: crontab (*/5 * * * *)
	•	Dashboard: Python, Plotly Dash
	•	Styling: Dash Bootstrap Components / custom CSS in assets/
	•	Virtual Environment: For isolated dependency management
	•	Reports: Python script auto-generates daily metrics 

---

 ## 🚀 Summary
	•	BTC-ETH Dashboard is a powerful crypto tracker built in Python
	•	Combines scraping, APIs, automation, and data visualization
	•	Designed for continuous data collection and real-time analytics
	•	A great way to learn about cron jobs, Dash apps, and time-series metrics
---

## 🤝 Contributing

We welcome contributions! To get started:
	1.	Fork the repository
	2.	Create a new branch (feature-name)
	3.	Submit a pull request ✅

For questions, reach out to:
👨‍💻 **[Bertan](https://github.com/Berkor10), [Mehdi](https://github.com/Dimeh91)!**

---

## 🚀 Stay tuned for upcoming releases!
