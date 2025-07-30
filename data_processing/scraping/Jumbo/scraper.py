import glob
import os
import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import boto3

PRODUCT_LINKS_FOLDER = "product_links"
BUCKET_NAME = "foodv-scraper-module"
S3_PREFIX = "Jumbo"
SCRAPE_LIMIT = 3  # We'll only scrape first 3 links per CSV

def expand_sections(driver):
    # If the text is already in HTML, this might be optional
    toggle_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-jum-action="toggleSection"]')
    for btn in toggle_buttons:
        try:
            btn.click()
            time.sleep(1)
        except:
            pass

def main():
    s3 = boto3.client("s3")
    driver = uc.Chrome(use_subprocess=True)

    for csvfile in glob.glob(os.path.join(PRODUCT_LINKS_FOLDER, "*.csv")):
        cat_name = os.path.splitext(os.path.basename(csvfile))[0].replace("links_", "")
        with open(csvfile, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            links = [row[0] for row in reader if row]

        for link in links[:SCRAPE_LIMIT]:
            driver.get(link)
            time.sleep(5)
            # If you want to expand sections (only if needed)
            expand_sections(driver)
            time.sleep(2)
            html = driver.page_source
            file_part = link.split("/")[-1] + ".html"
            key = f"{S3_PREFIX}/{cat_name}/{file_part}"
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=key,
                Body=html.encode("utf-8"),
                ContentType="text/html"
            )
            time.sleep(1)

    driver.quit()

if __name__ == "__main__":
    main()
