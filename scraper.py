import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

# Pulls the secret from GitHub Actions env
DB_CONNECTION_STRING = os.environ.get('DB_URL')

def save_to_database(data):
    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        cur = conn.cursor()
        insert_query = """
        INSERT INTO zomato_reviews_log (scrape_timestamp, restaurant_name, rating, delivery_rating_count, url)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            data['timestamp'],
            data['restaurant'],
            data['rating'],
            data['delivery_rating_count'],
            data['url']
        ))
        conn.commit()
        cur.close()
        conn.close()
        print("🛢️ Data successfully pushed to Neon!")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        raise e

def scrape_zomato_data():
    # Advanced targets for Market Intelligence
    targets = {
        "Meghana Foods": "https://www.zomato.com/bangalore/meghana-foods-indiranagar/reviews",
        "Empire Restaurant": "https://www.zomato.com/bangalore/empire-restaurant-indiranagar/reviews",
        "Nandhana Palace": "https://www.zomato.com/bangalore/nandhana-palace-indiranagar/reviews"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    print(f"🚀 Starting Advanced Market Analysis for {len(targets)} targets...")

    for name, url in targets.items():
        try:
            print(f"Scanning {name}...")
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                # Advanced logic: In a real scenario, we'd parse the specific numbers here.
                # For this step, we are logging the growth check.
                data_point = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "restaurant": name,
                    "rating": "4.4", # This would be scraped
                    "total_reviews": "70K", # This would be scraped
                    "url": url
                }
                save_to_database(data_point)
                print(f"✅ Logged {name}")
            else:
                print(f"⚠️ {name} blocked the scan (Status {response.status_code})")
        except Exception as e:
            print(f"❌ Failed to scan {name}: {e}")

if __name__ == "__main__":
    scrape_zomato_data()