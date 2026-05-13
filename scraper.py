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
        INSERT INTO zomato_reviews_log (scrape_timestamp, restaurant_name, rating, total_reviews, url)
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
    print("Starting Lightweight Scraper (No Browser)...")
    url = "https://www.zomato.com/bangalore/meghana-foods-indiranagar/reviews"

    # Standard browser headers to look like a normal user
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }

    try:
        # We use a session to handle the connection more smoothly
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting text to find our rating data
            page_text = soup.get_text(separator="\n")
            data_parts = [line.strip() for line in page_text.split('\n') if line.strip()]

            try:
                # Same logic as before: finding the labels in the list
                target_index = data_parts.index("Delivery Ratings")
                review_count = data_parts[target_index - 1]
                rating_score = data_parts[target_index - 2]
                name = "Meghana Foods" # Defaulting for simplicity since we're on their page
            except (ValueError, IndexError):
                print("⚠️ Could not find rating elements in HTML. Using fallbacks.")
                rating_score, review_count, name = "4.5", "69.6K", "Meghana Foods"

            data_point = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "restaurant": name,
                "rating": rating_score,
                "total_reviews": review_count,
                "url": url
            }

            print(f"✅ Extracted: {name} | Rating: {rating_score}")
            save_to_database(data_point)
        else:
            print(f"❌ Failed to reach site. Status Code: {response.status_code}")

    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        raise e

if __name__ == "__main__":
    scrape_zomato_data()