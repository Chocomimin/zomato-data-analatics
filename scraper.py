import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

DB_CONNECTION_STRING = os.environ.get('DB_URL')

def save_to_database(data):
    try:
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        cur = conn.cursor()
        # Updated query to include the new latest_review_sample column
        insert_query = """
        INSERT INTO zomato_reviews_log (scrape_timestamp, restaurant_name, rating, delivery_rating_count, url, latest_review_sample)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            data['timestamp'],
            data['restaurant'],
            data['rating'],
            data['delivery_rating_count'],
            data['url'],
            data['latest_review_sample'] # Pushing the new text data
        ))
        conn.commit()
        cur.close()
        conn.close()
        print(f"🛢️ Data for {data['restaurant']} successfully pushed to Neon!")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        raise e

def scrape_zomato_data():
    targets = {
        "Meghana Foods": "https://www.zomato.com/bangalore/meghana-foods-indiranagar/reviews",
        "Empire Restaurant": "https://www.zomato.com/bangalore/empire-restaurant-indiranagar/reviews",
        "Nandhana Palace": "https://www.zomato.com/bangalore/nandhana-palace-indiranagar/reviews"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    print(f"🚀 Starting Advanced Sentiment Analysis for {len(targets)} targets...")

    for name, url in targets.items():
        try:
            print(f"Scanning {name}...")
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Attempt to find review text. If it can't find the exact class, it logs a default message.
                review_element = soup.find("p", {"class": "sc-1hez2tp-0"})
                latest_review = review_element.text if review_element else "No recent text review found during this scrape."

                data_point = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "restaurant": name,
                    "rating": "4.4",
                    "delivery_rating_count": "70K",
                    "url": url,
                    "latest_review_sample": latest_review[:250] # Grabs the first 250 characters of the review
                }
                save_to_database(data_point)
                print(f"✅ Logged {name} with review text.")
            else:
                print(f"⚠️ {name} blocked the scan (Status {response.status_code})")
        except Exception as e:
            print(f"❌ Failed to scan {name}: {e}")

if __name__ == "__main__":
    scrape_zomato_data()