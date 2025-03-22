from smolagents import tool
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

@tool
def scrape_newegg_reviews_selenium(product_url: str) -> str:
    """
    Scrapes Newegg reviews using Selenium for a given product URL.

    Args:
    product_url (str): The full URL of the Newegg product page.

    Returns:
    str: A string of extracted reviews or an error message.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")

    service = Service("C:\\WebDriver\\bin\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        product_id = product_url.split("/p/")[-1].split("?")[0]
        review_url = f"https://www.newegg.com/p/{product_id}/reviews"

        driver.get(review_url)
        time.sleep(3)

        reviews = driver.find_elements(By.CLASS_NAME, "comments-content")
        if not reviews:
            return "No reviews found or reviews failed to load."

        review_texts = [r.text.strip() for r in reviews if r.text.strip()]
        return "\n\n".join(review_texts[:10])

    except Exception as e:
        return f"Error while scraping: {e}"

    finally:
        driver.quit()
