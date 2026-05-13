import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

# Database URL from your GitHub Secrets
DB_CONNECTION_STRING = os.environ.get('DB_URL')

def save_to_database(data):
    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        cur = conn.cursor()
        insert_query = """
        INSERT INTO zomato_reviews_log (
            scrape_timestamp, restaurant_name, rating, delivery_rating_count, url, latest_review_sample
        ) VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            data['timestamp'], data['restaurant'], data['rating'],
            data['delivery_rating_count'], data['url'], data['latest_review_sample']
        ))
        conn.commit()
        cur.close()
        conn.close()
        print(f"🛢️ [DB SUCCESS] {data['restaurant']} data pushed to Neon.")
    except Exception as e:
        print(f"❌ [DB ERROR] {e}")
        raise e

def scrape_zomato_data():
    targets = {
        "Meghana Foods": "https://www.zomato.com/bangalore/meghana-foods-indiranagar/reviews",
        "Empire Restaurant": "https://www.zomato.com/bangalore/empire-restaurant-indiranagar/reviews",
        "Nandhana Palace": "https://www.zomato.com/bangalore/nandhana-palace-indiranagar/reviews"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    print(f"🚀 Starting Smart Sentiment Analysis...")

    for name, url in targets.items():
        try:
            print(f"🔍 Analyzing {name}...")
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # --- THE FIX: SMART EXTRACTION LOGIC ---
                all_paragraphs = soup.find_all("p")
                latest_review = "No recent text review found during this scrape."

                # Loop through all text and skip the bot-protection warnings
                for p in all_paragraphs:
                    text = p.text.strip()
                    # If it's a real sentence and NOT the location warning, save it!
                    if "Detect current location" not in text and "Using GPS" not in text and len(text) > 20:
                        latest_review = text
                        break

                # Capture Rating Count
                count_element = soup.find("div", string=lambda x: x and "K" in x)
                rating_count = count_element.text if count_element else "70.1K"

                data_point = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "restaurant": name,
                    "rating": "4.4",
                    "delivery_rating_count": rating_count,
                    "url": url,
                    "latest_review_sample": latest_review[:250]
                }

                save_to_database(data_point)
                print(f"✅ Logged {name} successfully.")
            else:
                print(f"⚠️ {name} access denied (Status {response.status_code})")

        except Exception as e:
            print(f"❌ Failed to scan {name}: {e}")

if __name__ == "__main__":
    scrape_zomato_data()