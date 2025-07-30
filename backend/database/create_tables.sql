/* ----------------------------------------------------------
   0.  (Optional) create schema and set search_path
-----------------------------------------------------------*/
CREATE SCHEMA IF NOT EXISTS food;
SET search_path TO food;

/* ----------------------------------------------------------
   1.  STORES
-----------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS food.stores (
    store_id    serial PRIMARY KEY,
    name        varchar(60) UNIQUE NOT NULL,
    lat         numeric(9,6),
    lon         numeric(9,6),
    created_at  timestamp DEFAULT now()
);

/* ----------------------------------------------------------
   2.  PRODUCTS
-----------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS food.products (
    product_id       serial PRIMARY KEY,
    store_id         int NOT NULL REFERENCES food.stores(store_id),
    external_sku     varchar(120) NOT NULL UNIQUE,        -- external_sku alone is unique
    name             text,
    category         text,
    
    -- Flexible Unit System
    -- Examples:
    -- Avocado: unit_type='piece', unit_value=1, unit_description='per stuk'
    -- Potatoes: unit_type='weight', unit_value=1000, unit_description='1 KG'
    -- Milk: unit_type='volume', unit_value=1000, unit_description='1 L'
    unit_type        varchar(20),     -- 'weight', 'volume', 'piece', 'package'
    unit_value       numeric(10,2),   -- Numeric value (grams for weight, ml for volume, count for pieces)
    unit_description varchar(50),     -- Human readable ("1 KG", "per stuk", "500 ML")
    
    description      text,
    created_at       timestamp DEFAULT now(),
    country_of_origin text
);

/* ----------------------------------------------------------
   3.  PRICES  (history / snapshot table)
-----------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS food.prices (
    price_id       serial PRIMARY KEY,
    product_id     int NOT NULL REFERENCES food.products(product_id),
    scraped_at     timestamp NOT NULL DEFAULT now(),

    regular_price  numeric(10,2),
    promo_price    numeric(10,2),
    on_promotion   boolean      NOT NULL,
    promo_type     varchar(40),
    promo_text     text,
    price_per_kg   numeric(10,2),

    UNIQUE (product_id, scraped_at)             -- one snapshot per time-point
);

/* ----------------------------------------------------------
   4.  NUTRITION  (history / snapshot table)
   Note: All nutrition values are standardized per 100g/100ml for comparison
-----------------------------------------------------------*/
CREATE TABLE IF NOT EXISTS food.nutrition (
    nutrition_id  serial PRIMARY KEY,
    product_id    int NOT NULL REFERENCES food.products(product_id),
    scraped_at    timestamp DEFAULT now(),

    -- All values per 100g/100ml for standardization
    kcal_per_100g numeric(10,2),
    protein_per_100g numeric(10,2),
    fat_per_100g     numeric(10,2),
    carbs_per_100g   numeric(10,2),
    sodium_per_100g  numeric(10,2),
    fiber_per_100g   numeric(10,2),
    sugar_per_100g   numeric(10,2),
    
    raw_json      jsonb,              -- Store original nutrition data

    UNIQUE (product_id, scraped_at)
);

/* ----------------------------------------------------------
   5.  Helpful indexes for look-ups
-----------------------------------------------------------*/
CREATE INDEX IF NOT EXISTS idx_products_store     ON food.products (store_id);
CREATE INDEX IF NOT EXISTS idx_products_unit_type ON food.products (unit_type);
CREATE INDEX IF NOT EXISTS idx_prices_product     ON food.prices   (product_id);
CREATE INDEX IF NOT EXISTS idx_nutri_product      ON food.nutrition(product_id);
