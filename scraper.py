from playwright.sync_api import sync_playwright
import psycopg2
import time
from datetime import datetime

import os
# Pulls the secret from GitHub Actions env or uses local string for testing
DB_CONNECTION_STRING = os.environ.get('DB_URL', "your_local_test_string_here")


def save_to_database(data):
    try:
        # Connect to the Neon PostgreSQL database
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        cur = conn.cursor()

        # SQL Insert Command
        insert_query = """
        INSERT INTO zomato_reviews_log (scrape_timestamp, restaurant_name, rating, total_reviews, url)
        VALUES (%s, %s, %s, %s, %s);
        """

        # Execute the insert for the record
        cur.execute(insert_query, (
            data['timestamp'],
            data['restaurant'],
            data['rating'],
            data['total_reviews'],
            data['url']
        ))

        # Commit the transaction and close
        conn.commit()
        cur.close()
        conn.close()
        print(f"🛢️ Data successfully pushed to Neon Cloud!")

    except Exception as e:
        print(f"❌ Database Error: {e}")

def scrape_zomato_data():
    print("Starting Zomato Data Extractor (Mobile Stealth Mode)...")

    url = "https://www.zomato.com/bangalore/meghana-foods-indiranagar/reviews"

    with sync_playwright() as p:
        # Launching with specific window size and automation-hiding flags
        browser = p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox"
        ])

        # Emulate a real iPhone 13/14 Pro device
        device = p.devices['iPhone 14 Pro']
        context = browser.new_context(
            **device,
            locale="en-IN",
            timezone_id="Asia/Kolkata",
            extra_http_headers={"Referer": "https://www.google.com/"}
        )
        page = context.new_page()

        try:
            print(f"Navigating to: {url}")
            # Switching to 'networkidle' but with a shorter timeout to prevent hanging
            page.goto(url, wait_until="domcontentloaded", timeout=45000)

            # Wait for any H1 or just a fixed short delay for mobile rendering
            time.sleep(7)

            name = page.locator("h1").inner_text()
            raw_text = page.locator("body").inner_text()

            # Clean and split text
            data_parts = [line.strip() for line in raw_text.split('\n') if line.strip()]

            try:
                # Find exactly where "Delivery Ratings" is in our list
                target_index = data_parts.index("Delivery Ratings")
                review_count = data_parts[target_index - 1]
                rating_score = data_parts[target_index - 2]
            except ValueError:
                rating_score = "N/A"
                review_count = "N/A"

            data_point = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "restaurant": name,
                "rating": rating_score,
                "total_reviews": review_count,
                "url": url
            }

            print(f"✅ Extracted: {data_point['restaurant']} | Rating: {data_point['rating']}")
            save_to_database(data_point)

        except Exception as e:
            # If it fails, let's take a screenshot to see what's actually happening
            page.screenshot(path="error_state.png")
            print(f"❌ Failed to scrape. Saved error_state.png. Error: {e}")

        browser.close()
if __name__ == "__main__":
    scrape_zomato_data()