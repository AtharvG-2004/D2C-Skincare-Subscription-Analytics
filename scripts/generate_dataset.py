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

def generate_sessions(users_df, n_sessions=450000, seed=42):
    """Generate synthetic website sessions and funnel events."""

    random.seed(seed)

    traffic_sources = [
        "Paid Social",
        "Paid Search",
        "Influencer",
        "Email",
        "Organic Search",
        "Direct",
        "Referral",
    ]

    source_weights = {
        "Paid Social": 0.27,
        "Paid Search": 0.16,
        "Influencer": 0.12,
        "Email": 0.08,
        "Organic Search": 0.15,
        "Direct": 0.13,
        "Referral": 0.09,
    }

    landing_pages = [
        "Homepage",
        "Product Page",
        "Collection Page",
        "Skincare Quiz",
        "Subscription Landing",
        "Sale Landing",
    ]

    sessions = []

    for i in range(1, n_sessions + 1):
        user = users_df.iloc[random.randrange(len(users_df))]

        signup_date = pd.Timestamp(user["signup_date"])
        max_date = pd.Timestamp("2027-12-31")

        available_days = max(0, (max_date - signup_date).days)

        session_date = signup_date + pd.Timedelta(
            days=random.randint(0, available_days)
        )

        traffic_source = random.choices(
            traffic_sources,
            weights=[source_weights[x] for x in traffic_sources],
            k=1,
        )[0]

        device_type = user["device_type"]

        # Funnel probabilities by traffic source.
        product_view_prob = {
            "Paid Social": 0.62,
            "Paid Search": 0.72,
            "Influencer": 0.68,
            "Email": 0.78,
            "Organic Search": 0.70,
            "Direct": 0.75,
            "Referral": 0.76,
        }[traffic_source]

        add_cart_prob = {
            "Paid Social": 0.18,
            "Paid Search": 0.28,
            "Influencer": 0.22,
            "Email": 0.32,
            "Organic Search": 0.27,
            "Direct": 0.30,
            "Referral": 0.31,
        }[traffic_source]

        checkout_prob = {
            "Paid Social": 0.42,
            "Paid Search": 0.58,
            "Influencer": 0.48,
            "Email": 0.62,
            "Organic Search": 0.56,
            "Direct": 0.60,
            "Referral": 0.61,
        }[traffic_source]

        purchase_prob = {
            "Paid Social": 0.48,
            "Paid Search": 0.68,
            "Influencer": 0.55,
            "Email": 0.72,
            "Organic Search": 0.66,
            "Direct": 0.70,
            "Referral": 0.71,
        }[traffic_source]

        # Mobile users have slightly weaker checkout completion.
        if device_type == "Mobile":
            checkout_prob *= 0.95

        product_view = random.random() < product_view_prob

        add_to_cart = (
            product_view and random.random() < add_cart_prob
        )

        checkout_started = (
            add_to_cart and random.random() < checkout_prob
        )

        purchase_completed = (
            checkout_started and random.random() < purchase_prob
        )

        # Engagement metrics increase with funnel progression.
        base_duration = random.randint(15, 180)

        if product_view:
            base_duration += random.randint(20, 120)

        if add_to_cart:
            base_duration += random.randint(30, 120)

        if checkout_started:
            base_duration += random.randint(30, 150)

        if purchase_completed:
            base_duration += random.randint(20, 90)

        session_duration = base_duration

        pages_viewed = random.randint(1, 3)

        if product_view:
            pages_viewed += random.randint(1, 3)

        if add_to_cart:
            pages_viewed += random.randint(1, 2)

        if checkout_started:
            pages_viewed += 1

        landing_page = random.choice(landing_pages)

        sessions.append(
            {
                "session_id": f"S{i:06d}",
                "user_id": user["user_id"],
                "session_date": session_date.date(),
                "traffic_source": traffic_source,
                "landing_page": landing_page,
                "device_type": device_type,
                "session_duration_seconds": session_duration,
                "pages_viewed": pages_viewed,
                "product_view": product_view,
                "add_to_cart": add_to_cart,
                "checkout_started": checkout_started,
                "purchase_completed": purchase_completed,
            }
        )

    return pd.DataFrame(sessions)

def generate_subscriptions(users_df, n_subscriptions=18000, seed=42):
    """Generate synthetic skincare subscription records."""

    random.seed(seed)

    eligible_users = users_df.sample(
        n=min(n_subscriptions, len(users_df)),
        random_state=seed
    ).copy()

    plans = ["Basic", "Glow", "Premium"]
    plan_weights = [0.35, 0.45, 0.20]

    plan_prices = {
        "Basic": 699,
        "Glow": 999,
        "Premium": 1499,
    }

    frequencies = ["Monthly", "Quarterly"]
    frequency_weights = [0.80, 0.20]

    channels = {
        "Paid Social": 0.20,
        "Paid Search": 0.30,
        "Influencer": 0.22,
        "Email": 0.35,
        "Organic Search": 0.34,
        "Direct": 0.34,
        "Referral": 0.36,
    }

    cancel_reasons = [
        "Too expensive",
        "Product not needed",
        "Product dissatisfaction",
        "Payment failure",
        "Found alternative",
        "Too much product",
    ]

    rows = []

    for i, (_, user) in enumerate(eligible_users.iterrows(), start=1):

        signup_date = pd.Timestamp(user["signup_date"])
        end_date = pd.Timestamp("2027-12-31")

        available_days = max(0, (end_date - signup_date).days)

        # Subscription starts after signup.
        start_offset = random.randint(
            min(45, available_days),
            max(45, available_days)
        ) if available_days > 45 else available_days

        subscription_start = signup_date + pd.Timedelta(days=start_offset)

        if subscription_start > end_date:
            subscription_start = end_date

        plan = random.choices(
            plans,
            weights=plan_weights,
            k=1
        )[0]

        frequency = random.choices(
            frequencies,
            weights=frequency_weights,
            k=1
        )[0]

        monthly_price = plan_prices[plan]

        # Estimate lifecycle length.
        channel = user["acquisition_channel"]
        base_life = random.randint(4, 18)

        # Higher-quality channels retain customers longer.
        if channels.get(channel, 0.25) >= 0.30:
            base_life += random.randint(1, 5)

        if channel == "Paid Social":
            base_life -= random.randint(0, 3)

        if channel == "Influencer" and subscription_start.year >= 2027:
            base_life -= random.randint(1, 4)

        base_life = max(1, base_life)

        months_available = max(
            1,
            (end_date.year - subscription_start.year) * 12
            + end_date.month - subscription_start.month
            + 1
        )

        lifecycle_months = min(base_life, months_available)

        # Most subscriptions are active.
        status_roll = random.random()

        if lifecycle_months <= 2:
            status = random.choices(
                ["Active", "Cancelled"],
                weights=[0.75, 0.25],
                k=1
            )[0]
        else:
            status = random.choices(
                ["Active", "Cancelled", "Paused"],
                weights=[0.68, 0.24, 0.08],
                k=1
            )[0]

        cancel_date = None
        cancel_reason = None

        if status == "Cancelled":
            cancel_month = random.randint(1, lifecycle_months)

            cancel_date = subscription_start + pd.DateOffset(
                months=cancel_month
            )

            if cancel_date > end_date:
                cancel_date = end_date

            # About 8–12% of cancellations have no reason.
            if random.random() >= 0.10:
                cancel_reason = random.choice(cancel_reasons)

        # Initial estimate; later orders will provide the authoritative count.
        if frequency == "Monthly":
            total_cycles = lifecycle_months
        else:
            total_cycles = max(1, (lifecycle_months + 2) // 3)

        rows.append(
            {
                "subscription_id": f"SUB{i:05d}",
                "user_id": user["user_id"],
                "subscription_start_date": subscription_start.date(),
                "plan_type": plan,
                "billing_frequency": frequency,
                "monthly_price": monthly_price,
                "status": status,
                "cancel_date": (
                    cancel_date.date()
                    if cancel_date is not None
                    else None
                ),
                "cancel_reason": cancel_reason,
                "total_cycles": total_cycles,
            }
        )

    return pd.DataFrame(rows)