# 🍔 Zomato Real-Time Delivery Bottleneck Analyzer

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Web_Scraping-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon.tech-blue.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-orange.svg)
![Power BI](https://img.shields.io/badge/Power_BI-Analytics-yellow.svg)

An automated, cloud-based data pipeline designed to monitor and visualize live operational stress within food delivery networks, identifying localized gridlock before it cascades.

---

## 📖 Context & Background
Food delivery platforms rely on complex logistical networks to match customer orders with restaurant preparation times and delivery partner availability. A critical metric for user retention and operational efficiency is the Estimated Time of Arrival (ETA). Maintaining accurate ETAs requires continuous monitoring of restaurant throughput, especially in high-density urban zones during peak demand hours.

## ⚠️ The Problem
Unpredictable surges in order volume, adverse weather conditions, or local events frequently overwhelm specific restaurants, causing localized operational bottlenecks. When a restaurant's preparation time inflates rapidly, delivery partners are forced into prolonged idle times at the pickup location.

This creates a cascading gridlock effect:
* A localized shortage of delivery partners.
* Inflated ETAs across the immediate geographical radius.
* Dynamic pricing surges.
* Degradation of customer trust due to unmet delivery promises.

## 🎯 Project Objective
Currently, publicly available datasets for food delivery networks are static and historical, making them insufficient for identifying *live* bottlenecks.

This project solves this by engineering an end-to-end data pipeline to:
1. **Automate Extraction:** Deploy a scheduled web scraper (Playwright) to continuously extract live ETA and operational status data from a high-density cluster of restaurants.
2. **Maintain a Time-Series Ledger:** Structure and store this continuous data stream within a cloud-hosted relational database (PostgreSQL via Neon.tech).
3. **Visualize ETA Inflation:** Develop an interactive, real-time analytics dashboard (Power BI) to calculate and visualize "ETA Inflation Percentages," providing actionable intelligence to predict network gridlock.

---

## 🏗️ System Architecture

1. **Extraction (GitHub Actions + Playwright):** A Python script runs every 30 minutes via GitHub Actions, utilizing headless browser automation to extract live ETAs and surge tags.
2. **Storage (Neon.tech PostgreSQL):** The script sanitizes the data and executes a secure SQL `INSERT` to a cloud database, building a live time-series dataset.
3. **Analytics (Power BI):** A dashboard connects via DirectQuery to compute baseline ETAs and highlight active bottlenecks using DAX measures.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Automation & Scraping:** Playwright
* **CI/CD Pipeline:** GitHub Actions
* **Database:** PostgreSQL (Hosted on Neon.tech)
* **Business Intelligence:** Power BI

---

## 🚀 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/zomato-realtime-analytics.git](https://github.com/yourusername/zomato-realtime-analytics.git)
cd zomato-realtime-analytics