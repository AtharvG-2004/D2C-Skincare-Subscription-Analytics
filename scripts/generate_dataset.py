import random
import pandas as pd


def generate_product_catalog(n_products=80, seed=42):
    """Generate the synthetic skincare product catalog."""

    random.seed(seed)

    categories = {
        "Cleansers": ["Foam Cleanser", "Gel Cleanser", "Cream Cleanser"],
        "Moisturizers": ["Hydrating Cream", "Gel Moisturizer", "Barrier Cream"],
        "Serums": ["Vitamin C Serum", "Hyaluronic Serum", "Niacinamide Serum"],
        "Sunscreen": ["SPF 30 Sunscreen", "SPF 50 Sunscreen", "Mineral Sunscreen"],
        "Toners": ["Hydrating Toner", "Balancing Toner", "Exfoliating Toner"],
        "Face Masks": ["Clay Mask", "Hydrating Mask", "Detox Mask"],
        "Eye Care": ["Eye Cream", "Eye Gel", "Brightening Eye Serum"],
        "Body Care": ["Body Lotion", "Body Scrub", "Body Butter"],
    }

    category_weights = {
        "Cleansers": 0.14,
        "Moisturizers": 0.16,
        "Serums": 0.20,
        "Sunscreen": 0.15,
        "Toners": 0.10,
        "Face Masks": 0.09,
        "Eye Care": 0.06,
        "Body Care": 0.10,
    }

    products = []

    for i in range(1, n_products + 1):
        category = random.choices(
            list(category_weights.keys()),
            weights=list(category_weights.values()),
            k=1,
        )[0]

        product_type = random.choice(categories[category])

        # Pricing tiers
        tier = random.choices(
            ["Budget", "Core", "Premium", "Luxury"],
            weights=[0.25, 0.4375, 0.25, 0.0625],
            k=1,
        )[0]

        price_ranges = {
            "Budget": (299, 599),
            "Core": (600, 1099),
            "Premium": (1100, 1799),
            "Luxury": (1800, 2499),
        }

        min_price, max_price = price_ranges[tier]
        price = random.randint(min_price, max_price)

        # Margin profile
        margin_profile = random.choices(
            ["Low", "Standard", "High"],
            weights=[0.25, 0.50, 0.25],
            k=1,
        )[0]

        margin_ranges = {
            "Low": (0.25, 0.35),
            "Standard": (0.40, 0.55),
            "High": (0.55, 0.70),
        }

        min_margin, max_margin = margin_ranges[margin_profile]
        margin = random.uniform(min_margin, max_margin)

        cost = round(price * (1 - margin), 2)

        # Launch dates spread across the 3-year period
        launch_date = pd.Timestamp(
            "2025-01-01"
        ) + pd.Timedelta(days=random.randint(0, 1094))

        # Most products are subscription eligible
        is_subscription_eligible = random.random() < 0.70

        # Status depends partly on launch timing
        days_since_launch = (
            pd.Timestamp("2027-12-31") - launch_date
        ).days

        if days_since_launch > 700 and random.random() < 0.12:
            product_status = "Discontinued"
        elif random.random() < 0.08:
            product_status = "Seasonal"
        else:
            product_status = "Active"

        product_name = f"{product_type} {i:03d}"

        products.append(
            {
                "product_id": f"P{i:04d}",
                "product_name": product_name,
                "category": category,
                "product_type": product_type,
                "price": price,
                "cost": cost,
                "launch_date": launch_date.date(),
                "is_subscription_eligible": is_subscription_eligible,
                "product_status": product_status,
            }
        )

    return pd.DataFrame(products)