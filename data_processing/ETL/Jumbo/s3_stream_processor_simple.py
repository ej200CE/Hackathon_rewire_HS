"""
Simple S3 HTML Stream Processor - Focused on Specific Jumbo Data Extraction
This script extracts specific product data from Jumbo HTML files found via F12 inspection.
"""

import boto3
from bs4 import BeautifulSoup
import logging
import re

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class JumboDataExtractor:
    """
    A class to extract specific product data from Jumbo HTML files.
    """
    
    def __init__(self, bucket_name="foodv-scraper-module"):
        """
        Initialize the extractor with S3 client and bucket name.
        
        Args:
            bucket_name: The name of your S3 bucket
        """
        # Create S3 client - this connects to AWS
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        logger.info(f"Initialized Jumbo data extractor for bucket: {bucket_name}")
    
    def list_category_folders(self, prefix="Jumbo/"):
        """
        List all category folders in the S3 bucket.
        
        Args:
            prefix: The prefix to search for folders (e.g., "Jumbo/")
            
        Returns:
            List of folder names (categories)
        """
        logger.info(f"Listing folders with prefix: {prefix}")
        
        folders = set()
        
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix, Delimiter='/'):
                if 'CommonPrefixes' in page:
                    for prefix_info in page['CommonPrefixes']:
                        folder = prefix_info['Prefix']
                        category = folder.replace(prefix, '').rstrip('/')
                        folders.add(category)
            
            logger.info(f"Found {len(folders)} category folders")
            return sorted(list(folders))
            
        except Exception as e:
            logger.error(f"Error listing folders: {e}")
            return []
    
    def list_html_files_in_folder(self, folder_path):
        """
        List all HTML files in a specific folder.
        
        Args:
            folder_path: The S3 folder path (e.g., "Jumbo/aardappelen,-groente-en-fruit/")
            
        Returns:
            List of S3 keys for HTML files
        """
        logger.info(f"Listing HTML files in: {folder_path}")
        
        html_files = []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=folder_path
            )
            
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    if key.endswith('.html'):
                        html_files.append({
                            'key': key,
                            'size': obj['Size'],
                            'last_modified': obj['LastModified']
                        })
            
            logger.info(f"Found {len(html_files)} HTML files")
            return html_files
            
        except Exception as e:
            logger.error(f"Error listing HTML files: {e}")
            return []
    
    def stream_html_content(self, s3_key):
        """
        Stream HTML content from S3 without saving to disk.
        
        Args:
            s3_key: The S3 key of the HTML file
            
        Returns:
            The HTML content as a string, or None if error
        """
        logger.info(f"Streaming HTML from: {s3_key}")
        
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            html_content = response['Body'].read()
            html_string = html_content.decode('utf-8')
            
            logger.info(f"Successfully streamed HTML: {len(html_string)} characters")
            return html_string
            
        except Exception as e:
            logger.error(f"Error streaming HTML: {e}")
            return None
    
    def extract_product_data(self, html_content, s3_key=None):
        """
        Extract specific product data from HTML based on F12 inspection.
        
        Args:
            html_content: The HTML string
            s3_key: The S3 key/path (used to extract category from folder name)
            
        Returns:
            Dictionary with extracted product data
        """
        logger.info("Extracting specific Jumbo product data...")
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Initialize data structures matching database schema
        
        # Products table structure
        product = {
            'store_id': 1,              # Jumbo store_id (assuming 1 for now)
            'external_sku': None,       # Will extract from URL or generate
            'product_id': None,
            'name': None,
            'category': None,
            'unit_type': None,          # 'weight', 'volume', 'piece', 'package'
            'unit_value': None,         # Numeric value (grams/ml/count)
            'unit_description': None,   # Human readable ("1 KG", "per stuk")
            'description': None,
        }
        
        # Prices table structure
        price = {
            'product_id': None,
            'scraped_at': None,
            'regular_price': None,
            'promo_price': None,
            'on_promotion': False,      # Default to False
            'promo_type': None,
            'promo_text': None,
            'price_per_kg': None,
        }
        
        # Nutrition table structure  
        nutrition = {
            'nutrition_id': None,
            'product_id': None,
            'scraped_at': None,
            'kcal_per_100g': None,
            'protein_per_100g': None,
            'fat_per_100g': None,
            'carbs_per_100g': None,
            'sodium_per_100g': None,
            'fiber_per_100g': None,
            'sugar_per_100g': None,
            'raw_json': None,
        }
        
        # Extract category from S3 key
        # S3 key format: "Jumbo/category-name/product.html"
        if s3_key:
            logger.info("Extracting category from S3 path...")
            path_parts = s3_key.split('/')
            if len(path_parts) >= 2:
                # Get the category (second part of path after "Jumbo/")
                category = path_parts[1]
                product['category'] = category
                logger.info(f"✓ Found category: {product['category']}")
            else:
                logger.warning("✗ Could not extract category from S3 path")
        else:
            logger.info("ℹ No S3 key provided, cannot extract category")
        
        # 1. Extract Product Name
        # Looking for: h1 with data-testid="product-title"
        logger.info("Extracting product name...")
        product_name_element = soup.find('h1', {'data-testid': 'product-title'})
        if product_name_element:
            product['name'] = product_name_element.get_text(strip=True)
            logger.info(f"✓ Found product name: {product['name']}")
        else:
            logger.warning("✗ Product name not found")
        
        # 2. Extract Product Price
        # Looking for: div with data-testid="product_price" then nested screenreader-only div
        logger.info("Extracting product price...")
        price_container = soup.find('div', {'data-testid': 'product-price'})
        if price_container:
            logger.info("Found price container")
            screenreader_div = price_container.find('div', class_='screenreader-only')
            if screenreader_div:
                price_text = screenreader_div.get_text(strip=True)
                logger.info(f"Found price text: {price_text}")
                # Extract price from text like "Prijs: €2,19"
                price_match = re.search(r'€\s*(\d+[,\.]\d+)', price_text.replace(',', '.'))
                if price_match:
                    price_value = float(price_match.group(1))
                    price['regular_price'] = price_value
                    logger.info(f"✓ Found product price: €{price['regular_price']}")
                else:
                    logger.warning(f"Could not parse price from: {price_text}")
            else:
                logger.warning("✗ Price screenreader div not found")
        else:
            logger.warning("✗ Price container not found")
        
        # 3. Extract Product Weight/Unit
        # Looking for: span with data-testid="product_subtitle"
        logger.info("Extracting product weight/unit...")
        weight_element = soup.find('span', {'data-testid': 'product-subtitle'})
        if weight_element:
            unit_text = weight_element.get_text(strip=True)
            logger.info(f"Found unit text: {unit_text}")
            
            # Parse unit text into flexible unit system
            unit_type, unit_value, unit_description = self._parse_unit_text(unit_text)
            product['unit_type'] = unit_type
            product['unit_value'] = unit_value
            product['unit_description'] = unit_description
            
            # Set price_per_kg if it's a weight item
            if unit_type == 'weight' and unit_value and price['regular_price']:
                # Calculate price per kg (unit_value is in grams)
                price_per_gram = price['regular_price'] / unit_value
                price['price_per_kg'] = price_per_gram * 1000  # Convert to per kg
                
            logger.info(f"✓ Parsed unit: type={unit_type}, value={unit_value}, desc={unit_description}")
        else:
            logger.info("ℹ Product weight not found (assuming per piece)")
            product['unit_type'] = 'piece'
            product['unit_value'] = 1
            product['unit_description'] = 'per stuk'
        
        # 4. Extract external_sku from product URL
        logger.info("Extracting external_sku from product URL...")
        # Look for canonical URL or product URL in meta tags
        canonical_link = soup.find('link', {'rel': 'canonical'})
        product_url = None
        
        if canonical_link and canonical_link.get('href'):
            product_url = canonical_link.get('href')
            logger.info(f"Found canonical URL: {product_url}")
        
        if product_url:
            # Extract SKU from URL pattern: everything after last "-" before query params
            # Example: https://www.jumbo.com/producten/aardappelen-kriel-geel-1-kg-657405ZK
            url_parts = product_url.split('?')[0]  # Remove query params
            url_segments = url_parts.split('-')
            if len(url_segments) > 1:
                external_sku = url_segments[-1]  # Last part after final "-"
                product['external_sku'] = external_sku
                logger.info(f"✓ Found external_sku: {external_sku}")
            else:
                logger.warning("Could not parse external_sku from URL")
                # Fallback to filename-based SKU
                if s3_key:
                    filename = s3_key.split('/')[-1].replace('.html', '')
                    product['external_sku'] = f"jumbo_{filename}"
        else:
            logger.warning("✗ Product URL not found, using fallback")
            # Fallback to filename-based SKU
            if s3_key:
                filename = s3_key.split('/')[-1].replace('.html', '')
                product['external_sku'] = f"jumbo_{filename}"
        
        # 5. Store id
        product['store_id'] = 1
        
        return {
            'product': product,
            'price': price,
            'nutrition': nutrition,
            
        }
    
    def _parse_unit_text(self, unit_text):
        """
        Parse unit text into flexible unit system for database storage.
        
        Args:
            unit_text: String like "1 KG", "500 ML", "per stuk", "6 stuks"
            
        Returns:
            tuple: (unit_type, unit_value, unit_description)
                unit_type: 'weight', 'volume', 'piece', 'package'
                unit_value: numeric value in base units (grams/ml/count)
                unit_description: human readable string
        """
        if not unit_text:
            return 'piece', 1, 'per stuk'
        
        unit_text_lower = unit_text.lower().strip()
        
        # Weight patterns (convert to grams)
        weight_patterns = [
            (r'(\d+(?:[.,]\d+)?)\s*kg', lambda x: ('weight', float(x.replace(',', '.')) * 1000, unit_text)),
            (r'(\d+(?:[.,]\d+)?)\s*g(?:ram)?', lambda x: ('weight', float(x.replace(',', '.')), unit_text)),
        ]
        
        # Volume patterns (convert to ml)
        volume_patterns = [
            (r'(\d+(?:[.,]\d+)?)\s*l(?:iter)?', lambda x: ('volume', float(x.replace(',', '.')) * 1000, unit_text)),
            (r'(\d+(?:[.,]\d+)?)\s*ml', lambda x: ('volume', float(x.replace(',', '.')), unit_text)),
        ]
        
        # Piece patterns
        piece_patterns = [
            (r'(\d+)\s*stuks?', lambda x: ('piece', int(x), unit_text)),
            (r'per\s*stuk', lambda x: ('piece', 1, unit_text)),
        ]
        
        # Try weight patterns
        for pattern, converter in weight_patterns:
            match = re.search(pattern, unit_text_lower)
            if match:
                return converter(match.group(1))
        
        # Try volume patterns  
        for pattern, converter in volume_patterns:
            match = re.search(pattern, unit_text_lower)
            if match:
                return converter(match.group(1))
        
        # Try piece patterns
        for pattern, converter in piece_patterns:
            match = re.search(pattern, unit_text_lower)
            if match:
                return converter(match.group(1))
        
        # Default fallback
        return 'package', 1, unit_text
    
    def process_single_file(self):
        """
        Main method to process a single file and extract product data.
        """
        logger.info("=" * 50)
        logger.info("Starting Jumbo Product Data Extraction")
        logger.info("=" * 50)
        
        # Step 1: Get first category
        categories = self.list_category_folders()
        if not categories:
            logger.warning("No categories found!")
            return
        
        first_category = categories[0]
        logger.info(f"\nProcessing category: {first_category}")
        
        # Step 2: Get first HTML file
        folder_path = f"Jumbo/{first_category}/"
        html_files = self.list_html_files_in_folder(folder_path)
        if not html_files:
            logger.warning(f"No HTML files found in {folder_path}")
            return
        
        first_file = html_files[0]
        logger.info(f"\nProcessing file: {first_file['key']}")
        logger.info(f"File size: {first_file['size'] / 1024:.2f} KB")
        
        # Step 3: Stream and extract data
        html_content = self.stream_html_content(first_file['key'])
        if not html_content:
            logger.error("Failed to stream HTML content")
            return
        
        # Step 4: Extract product data
        extracted_data = self.extract_product_data(html_content, first_file['key'])
        
        # Step 5: Display results
        logger.info("\n" + "=" * 50)
        logger.info("EXTRACTED PRODUCT DATA")
        logger.info("=" * 50)
        
        product_data = extracted_data['product']
        price_data = extracted_data['price']
        nutrition_data = extracted_data['nutrition']
        
        print(f"\n--- PRODUCT INFO ---")
        print(f"Name: {product_data['name'] or 'NOT FOUND'}")
        print(f"Category: {product_data['category'] or 'NOT FOUND'}")
        print(f"External SKU: {product_data['external_sku'] or 'NOT FOUND'}")
        print(f"Unit Type: {product_data['unit_type'] or 'NOT FOUND'}")
        print(f"Unit Value: {product_data['unit_value'] or 'NOT FOUND'}")
        print(f"Unit Description: {product_data['unit_description'] or 'NOT FOUND'}")
        
        print(f"\n--- PRICING INFO ---")
        print(f"Regular Price: €{price_data['regular_price'] or 'NOT FOUND'}")
        print(f"Price per KG: €{price_data['price_per_kg'] or 'N/A'}")
        print(f"On Promotion: {price_data['on_promotion']}")
        
        print(f"\n--- NUTRITION INFO ---")
        print(f"Calories per 100g: {nutrition_data['kcal_per_100g'] or 'NOT FOUND'}")
        print(f"Protein per 100g: {nutrition_data['protein_per_100g'] or 'NOT FOUND'}")
        print(f"Carbs per 100g: {nutrition_data['carbs_per_100g'] or 'NOT FOUND'}")
        
        logger.info("=" * 50)
        logger.info("Extraction complete!")
        logger.info("=" * 50)
        
        return extracted_data


def main():
    """
    Main function to run the extractor.
    """
    extractor = JumboDataExtractor()
    extractor.process_single_file()


if __name__ == "__main__":
    main() 