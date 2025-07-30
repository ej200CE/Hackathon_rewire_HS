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
os.environ["LOG_TO_STDOUT"] = "true"

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

    def parse_html(self, key: str):
        s3 = self.s3_connect()
        body = s3.get_object(Bucket = self.bucket, Key=key)["Body"].read()

        soup = BeautifulSoup(body, "lxml")


        ### ─────────── Products table ─────────── ###

        # 1. Find title
        title_tag = soup.find("h1", attrs={"data-testid": "product-title"})
        if title_tag:
            title = title_tag.get_text(strip=True)
            logger.info("%s", title) 
        else:
            logger.warning("No title found in %s", key)


        # Putting it all together into a data structure and yielding as a dictionary
        prod_row = ProductRow(
            store_id=1,                     # Jumbo
            external_sku=key.split("-")[-1].split(".")[0],  # SKU from filename
            name=title
        )
        
        return {
            "product": prod_row
        }

    def run(self):
        logger.info("Initializing S3 parser...")

        for key in self.iterate_html_keys():
            row = self.parse_html(key)
            prod = row["product"]
        
        logger.info("S3 fully parsed.")


if __name__ == "__main__":
    parser = JumboHTMLParser(Bucket, Prefix, db_url)
    parser.run()
