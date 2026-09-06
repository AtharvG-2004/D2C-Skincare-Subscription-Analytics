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

def generate_users(n_users=60000, start_date="2025-01-01", end_date="2027-12-31", seed=42):
    """Generate the synthetic user/customer table."""

    random.seed(seed)

    channels = [
        "Paid Social",
        "Paid Search",
        "Influencer",
        "Email",
        "Organic Search",
        "Direct",
        "Referral",
    ]

    channel_weights = [0.27, 0.16, 0.12, 0.08, 0.15, 0.13, 0.09]

    campaigns = {
        "Paid Social": [
            "Meta_Skincare_Prospecting",
            "Meta_Glow_Campaign",
            "Instagram_Skincare",
        ],
        "Paid Search": [
            "Google_Brand_Search",
            "Google_Skincare_Search",
            "Google_Product_Search",
        ],
        "Influencer": [
            "Creator_Glow_Campaign",
            "Beauty_Influencer_2025",
            "Skincare_Creators",
        ],
        "Email": [
            "Welcome_Series",
            "Product_Recommendations",
            "Reactivation_Email",
        ],
        "Organic Search": [
            "SEO_Skincare",
            "SEO_Beauty_Guides",
            "Organic_Product_Search",
        ],
        "Direct": ["Direct"],
        "Referral": [
            "Customer_Referral",
            "Friend_Referral",
        ],
    }

    devices = ["Mobile", "Desktop", "Tablet"]
    device_weights = [0.70, 0.25, 0.05]

    age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]
    age_weights = [0.12, 0.38, 0.28, 0.15, 0.07]

    genders = ["Female", "Male", "Non-binary", "Prefer not to say"]
    gender_weights = [0.68, 0.25, 0.02, 0.05]

    locations = {
        "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
        "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru"],
        "Delhi": ["New Delhi"],
        "Telangana": ["Hyderabad", "Warangal"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
        "West Bengal": ["Kolkata"],
        "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
        "Rajasthan": ["Jaipur", "Udaipur"],
        "Kerala": ["Kochi", "Thiruvananthapuram"],
    }

    states = list(locations.keys())
    state_weights = [
        0.22, 0.14, 0.10, 0.08, 0.10,
        0.09, 0.06, 0.08, 0.05, 0.08
    ]

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    days = (end - start).days

    rows = []

    for i in range(1, n_users + 1):

        # Slight growth in user acquisition over time.
        # Squared random value produces more users in later periods.
        signup_offset = int((random.random() ** 0.85) * days)
        signup_date = start + pd.Timedelta(days=signup_offset)

        channel = random.choices(
            channels,
            weights=channel_weights,
            k=1
        )[0]

        campaign = random.choice(campaigns[channel])

        # Controlled missing campaign values (~2.5%)
        if random.random() < 0.025:
            campaign = None

        device = random.choices(
            devices,
            weights=device_weights,
            k=1
        )[0]

        age_group = random.choices(
            age_groups,
            weights=age_weights,
            k=1
        )[0]

        gender = random.choices(
            genders,
            weights=gender_weights,
            k=1
        )[0]

        state = random.choices(
            states,
            weights=state_weights,
            k=1
        )[0]

        city = random.choice(locations[state])

        # Controlled demographic missingness.
        if random.random() < 0.025:
            age_group = None

        if random.random() < 0.025:
            gender = None

        if random.random() < 0.015:
            city = None

        rows.append(
            {
                "user_id": f"U{i:05d}",
                "signup_date": signup_date.date(),
                "acquisition_channel": channel,
                "acquisition_campaign": campaign,
                "device_type": device,
                "age_group": age_group,
                "gender": gender,
                "city": city,
                "state": state,
                "first_purchase_date": None,
                "customer_status": "Prospect",
            }
        )

    return pd.DataFrame(rows)