import os
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def insert_data(brand, price, original_price, delivery_price, ratings, ratings_num, ratings_link, link, image_link):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO watch_data (brand, price, original_price, delivery_price, ratings, ratings_num, ratings_link, link, image_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (brand, price, original_price, delivery_price, ratings, ratings_num, ratings_link, link, image_link))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error inserting data: {e}")

def scrape_amazon():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.amazon.com")
        print("Navigated to Amazon.")
        wait = WebDriverWait(driver, 15)  # Increased wait time
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))
        print("Search box found.")
        search_box.send_keys("watches")
        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'nav-search-submit-button')))
        search_button.click()
        print("Clicked the search button.")

        while True: 
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            print("Search results loaded.")

            watch_items = driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')
            print(f"Found {len(watch_items)} watch items.")

            for item in watch_items:
                try:
                    brand = item.find_element(By.XPATH, './/h2/a/span').text
                    print(f"Scraping item: {brand}")
                    
                    price = "Not available"
                    try:
                        price_whole = wait.until(EC.visibility_of_element_located((By.XPATH, './/span[@class="a-price-whole"]')))
                        price_fraction = wait.until(EC.visibility_of_element_located((By.XPATH, './/span[@class="a-price-fraction"]')))
                        price = f"{price_whole.text}.{price_fraction.text}"
                        print(f"Price found: {price}")
                    except Exception as e:
                        print("Price element not found or error:", e)

                    delivery_price = "Not available"
                    try:
                        delivery_price_element = wait.until(
                            EC.presence_of_element_located((By.XPATH, './/div[@data-cy="delivery-recipe"]//span[@aria-label]'))
                        )
                        delivery_price = delivery_price_element.text
                        print(f"Delivery price found: {delivery_price}")
                    except:
                        delivery_price = "Not available"

                    original_price = "Not available"
                    try:
                        original_price_element = wait.until(EC.presence_of_element_located((By.XPATH, './/span[@class="a-price a-text-price"]/span[@class="a-offscreen"]')))
                        original_price = original_price_element.text
                        print(f"Original price found: {original_price}")
                    except:
                        original_price = "Not available"

                    ratings = "Not available"
                    ratings_num = "Not available"
                    ratings_link = "Not available"
                    try:
                        ratings_element = item.find_element(By.XPATH, './/i[@data-cy="reviews-ratings-slot"]/span[@class="a-icon-alt"]')
                        ratings = ratings_element.text
                        
                        ratings_num_element = item.find_element(By.XPATH, './/span[@data-component-type="s-client-side-analytics"]//span[@aria-label]')
                        ratings_num = ratings_num_element.text
                        
                        ratings_link = item.find_element(By.XPATH, './/h2/a').get_attribute("href")
                    except:
                        ratings = "Not available"
                        ratings_num = "Not available"
                        ratings_link = "Not available"

                    link = item.find_element(By.XPATH, './/h2/a').get_attribute("href")
                    image_link = item.find_element(By.XPATH, './/img[@class="s-image"]').get_attribute("src")

                    insert_data(brand, price, original_price, delivery_price, ratings, ratings_num, ratings_link, link, image_link)
                    
                except Exception as e:
                    print(f"Error scraping item: {e}")

            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="s-pagination-next"]')))
                if "a-disabled" in next_button.get_attribute("class"):
                    print("No more pages to navigate.")
                    break
                next_button.click()
                print("Navigating to the next page.")
            except Exception as e:
                print(f"Error finding the next page button: {e}")
                break

    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watch_data (
                id SERIAL PRIMARY KEY,
                brand TEXT,
                price TEXT,
                original_price TEXT,
                delivery_price TEXT,
                ratings TEXT,
                ratings_num TEXT,
                ratings_link TEXT,
                link TEXT,
                image_link TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

    # Start scraping
    scrape_amazon()
