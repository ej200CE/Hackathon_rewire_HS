from pathlib import Path
from typing import Iterable, Iterator
from dataclasses import dataclass, asdict
from datetime import datetime
import boto3
from bs4 import BeautifulSoup
import logging
from shared.log import auto_setup_logger 
from shared.models import ProductRow, PriceRow, NutritionRow


import os 
os.environ["LOG_TO_STDOUT"] = "false"

auto_setup_logger()
logger = logging.getLogger(__name__)


# ─────────── S3 connection ─────────── #
Bucket = "foodv-scraper-module"
Prefix = "Jumbo/"
db_url = "dummy_url"


class JumboHTMLParser:
    def __init__(self, bucket: str, prefix: str, db_url: str, ):
        self.bucket = bucket
        self.prefix = prefix
        self.db_link = db_url
        self._s3: boto3.client | None = None

    def s3_connect(self):
        if self._s3 is None: 
            logging.info("Creating boto3 client")
            self._s3 = boto3.client("s3")
            self._s3.head_bucket(Bucket=self.bucket)
            logging.info("Connection to S3 successfull -> bucket %s", self.bucket)
        return self._s3
    
    def iterate_html_keys(self):
        s3 = self.s3_connect()
        paginator = s3.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket = self.bucket, 
                                       Prefix = self.prefix, 
                                       PaginationConfig={"PageSize": 1000}
                                       ):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if key.lower().endswith(".html"):
                    yield key

    def load_html(self, key: str):
        s3 = self.s3_connect()
        body = s3.get_object(Bucket = self.bucket, Key=key)["Body"].read()
        return body

    def parse_html(self, content: bytes, key:str):

        soup = BeautifulSoup(content, "lxml")

        ### ─────────── Products table ─────────── ###

        # 1. Find title
        title_tag = soup.find("h1", attrs={"data-testid": "product-title"})
        if title_tag:
            title = title_tag.get_text(strip=True)
            #logger.info("%s", title) 
        else:
            logger.warning("No title found in %s", key)

        # 2. Get SKU from filename
        SKU = key.split("-")[-1].split(".")[0] 

        # 3. Get category from filename
        without_prefix = key[len(Prefix):]
        category_path = without_prefix.split("/")[0]

        # 4. Find unit type
        ppu_div = soup.find("div", class_="price-per-unit")
        if ppu_div:
            # Get all spans inside the price-per-unit div
            spans = ppu_div.find_all("span", attrs={"aria-hidden": "true"})
            if len(spans) >= 3:
                # Typically: [price, "/", unit] - we want the last one
                unit_text = spans[-1].get_text(strip=True).lower()
                if "kilo" in unit_text or "kg" in unit_text:
                    unit_type = "weight"
                    unit_value = 1000  # grams
                    unit_desc = "1 kilogram"
                elif "gram" in unit_text or "grams" in unit_text:
                    unit_type = "weight" 
                    unit_value = 1  # grams
                    unit_desc = f"1 {unit_text.upper()}"
                elif "liter" in unit_text or "l" == unit_text:
                    unit_type = "volume"
                    unit_value = 1000  # ml
                    unit_desc = "1 liter"
                elif "ml" in unit_text:
                    unit_type = "volume"
                    unit_value = int(''.join(filter(str.isdigit, unit_text)) or 1)
                    unit_desc = unit_text.upper()
                elif "stuk" in unit_text or "stuks" in unit_text or "stukken" in unit_text:
                    unit_type = "piece"
                    unit_value = 1
                    unit_desc = "per stuk"
                else:
                    unit_type = "package"
                    unit_value = 1
                    unit_desc = unit_text
            else:
                logger.warning("Expected 3 spans in price-per-unit for %s, found %d", key, len(spans))
                unit_type = unit_value = unit_desc = None
        else:
            logger.warning("No price-per-unit div found for %s", key)
            unit_type = unit_value = unit_desc = None

        # 5. Find product description (if any)
        description = None
        desc_div = soup.find("div", attrs={"data-testid": "product-description-text-body"})
        if desc_div:
            parts = []
            for el in desc_div.find_all(["p", "li"]):
                text = el.get_text(separator=" ", strip=True)
                if text:
                    parts.append(text)
            if parts:
                description = "\n".join(parts)
        
        # 6. Find land of origin of a specific product
        origin_div = soup.find("div", attrs={"data-testid":"origin-collapsible"})
        country_of_origin = None
        if origin_div:
            inner_div = origin_div.find("div")
            if inner_div:
                content_div = inner_div.find("div", class_="content")
                if content_div:
                    p_tag = content_div.find("p")
                    if p_tag:
                        origin_text = p_tag.get_text(strip=True)
                        if origin_text and len(origin_text) < 30:
                            country_of_origin = origin_text
        

        # Putting it all together into a data structure and yielding as a dictionary
        prod_row = ProductRow(
            store_id = 1,                     # Jumbo
            external_sku = SKU,  # SKU from filename
            name = title,
            category = category_path,
            unit_type = unit_type,
            unit_value = unit_value,
            unit_description = unit_desc,
            description = description,
            country_of_origin = country_of_origin
        )

        ### ─────────── Nutrition table ─────────── ###

        ### ─────────── Prices table ─────────── ###
        
        return {
            "product": prod_row
        }

    def run(self):
        logger.info("Initializing S3 parser...")

        for key in self.iterate_html_keys():
            html = self.load_html(key)
            result = self.parse_html(html, key)
        
        logger.info("S3 fully parsed.")


if __name__ == "__main__":
    parser = JumboHTMLParser(Bucket, Prefix, db_url)
    parser.run()

