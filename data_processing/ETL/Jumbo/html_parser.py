from pathlib import Path
from typing import Iterable, Iterator
import boto3
from bs4 import BeautifulSoup
import logging
from shared.log import auto_setup_logger 

import os 
os.environ["LOG_TO_STDOUT"] = "true"

auto_setup_logger()
logger = logging.getLogger(__name__)


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

    def stream_html_key(self):

    def parse_html(self):

    def save_batches(self):
    
    def run():


