from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Any

# ─────────── products ───────────
@dataclass
class ProductRow:
    # columns in food.products
    store_id: int
    external_sku: str
    name: Optional[str] = None
    category: Optional[str] = None
    unit_type: Optional[str] = None          # 'weight', 'volume', 'piece', 'package'
    unit_value: Optional[float] = None
    unit_description: Optional[str] = None
    description: Optional[str] = None
    country_of_origin: Optional[str] = None
    # created_at is DB‑default (now()); no need to set here
    # product_id (PK) will be assigned by DB on insert

# ─────────── prices snapshot ───────────
@dataclass
class PriceRow:
    # FK link
    product_id: int
    # snapshot timestamp (default = now UTC)
    scraped_at: datetime = datetime.utcnow()
    regular_price: Optional[float] = None
    promo_price: Optional[float] = None
    on_promotion: bool = False
    promo_type: Optional[str] = None
    promo_text: Optional[str] = None
    price_per_kg: Optional[float] = None
    # price_id is serial PK, assigned by DB

# ─────────── nutrition snapshot ───────────
@dataclass
class NutritionRow:
    product_id: int
    scraped_at: datetime = datetime.utcnow()
    kcal_per_100g: Optional[float] = None
    protein_per_100g: Optional[float] = None
    fat_per_100g: Optional[float] = None
    carbs_per_100g: Optional[float] = None
    sodium_per_100g: Optional[float] = None
    fiber_per_100g: Optional[float] = None
    sugar_per_100g: Optional[float] = None
    raw_json: Optional[Any] = None
    # nutrition_id auto‑assigned by DB