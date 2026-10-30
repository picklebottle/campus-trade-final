import os
from datetime import datetime, timezone, timedelta
from app.database import Base, engine, SessionLocal
from app.models import User, Item, ItemImage, WishlistEntry, Conversation, Message
from app.auth import get_password_hash

def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data if any
    db.query(Message).delete()
    db.query(Conversation).delete()
    db.query(WishlistEntry).delete()
    db.query(ItemImage).delete()
    db.query(Item).delete()
    db.query(User).delete()
    db.commit()

    print("Populating database with seed data...")

    # 1. Users
    alex = User(
        name="Alex Rivera",
        email="alex@campus.edu",
        hashed_password=get_password_hash("password123"),
        college="Stanford University",
        department="Computer Science",
        year="3rd Year",
        rating=4.9,
        profile_views=38,
        created_at=datetime.now(timezone.utc) - timedelta(days=90)
    )
    priya = User(
        name="Priya Sharma",
        email="priya@campus.edu",
        hashed_password=get_password_hash("password123"),
        college="Stanford University",
        department="Electrical Engineering",
        year="2nd Year",
        rating=5.0,
        profile_views=24,
        created_at=datetime.now(timezone.utc) - timedelta(days=60)
    )
    marcus = User(
        name="Marcus Vance",
        email="marcus@campus.edu",
        hashed_password=get_password_hash("password123"),
        college="Stanford University",
        department="Mechanical Engineering",
        year="4th Year",
        rating=4.8,
        profile_views=52,
        created_at=datetime.now(timezone.utc) - timedelta(days=120)
    )
    sarah = User(
        name="Sarah Jenkins",
        email="sarah@campus.edu",
        hashed_password=get_password_hash("password123"),
        college="Stanford University",
        department="Product Design",
        year="1st Year",
        rating=5.0,
        profile_views=16,
        created_at=datetime.now(timezone.utc) - timedelta(days=30)
    )

    db.add_all([alex, priya, marcus, sarah])
    db.commit()
    db.refresh(alex)
    db.refresh(priya)
    db.refresh(marcus)
    db.refresh(sarah)

    # 2. Items with realistic imagery and descriptions
    items_data = [
        # Calculators
        {
            "title": "TI-84 Plus CE Color Graphing Calculator",
            "description": "Mint condition TI-84 Plus CE in Python Edition blue. Rechargeable battery holds charge for weeks. Includes original charging cable and protective slide cover. Essential for MATH 51/52 and stats courses.",
            "price": 3800,
            "category": "calculators",
            "condition": "Like new",
            "status": "active",
            "seller_id": alex.id,
            "days_ago": 1,
            "images": [
                "https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1587145820266-a5951ee6f620?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Casio fx-991EX ClassWiz Scientific Calculator",
            "description": "High-resolution solar/battery engineering calculator. Used for one semester of physics and chem. No scratches, clean screen, all matrix and complex math functions tested and working perfectly.",
            "price": 850,
            "category": "calculators",
            "condition": "Like new",
            "status": "active",
            "seller_id": marcus.id,
            "days_ago": 4,
            "images": [
                "https://images.unsplash.com/photo-1587145820266-a5951ee6f620?auto=format&fit=crop&w=800&q=80"
            ]
        },

        # Books
        {
            "title": "Introduction to Algorithms (CLRS) 4th Edition",
            "description": "The quintessential algorithms textbook. Hardcover 4th Edition with the updated machine learning and graph algorithms chapters. Crisp clean pages, no highlighter or pen markings.",
            "price": 1450,
            "category": "books",
            "condition": "Like new",
            "status": "active",
            "seller_id": priya.id,
            "days_ago": 2,
            "images": [
                "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Calculus: Early Transcendentals 9th Ed - Stewart",
            "description": "Official Stewart Calculus text for freshman and sophomore engineering. Minor corner wear on spine, interior is completely unmarked and binding is solid.",
            "price": 950,
            "category": "books",
            "condition": "Good condition",
            "status": "active",
            "seller_id": alex.id,
            "days_ago": 5,
            "images": [
                "https://images.unsplash.com/photo-1532012164546-f432f2e3777f?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
            "description": "Robert C. Martin's legendary software engineering book. Read once, paperback in pristine shape. Great read for interview prep and internship code reviews.",
            "price": 600,
            "category": "books",
            "condition": "Like new",
            "status": "active",
            "seller_id": sarah.id,
            "days_ago": 8,
            "images": [
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=800&q=80"
            ]
        },

        # Electronics
        {
            "title": "Sony WH-1000XM4 Noise Canceling Headphones",
            "description": "Industry leading active noise cancellation — perfect for studying in crowded dorms or the campus library. Fresh replacement ear pads installed last month. Comes with hard carry case and aux cord.",
            "price": 11500,
            "category": "electronics",
            "condition": "Good condition",
            "status": "active",
            "seller_id": alex.id,
            "days_ago": 2,
            "images": [
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Dell UltraSharp 24\" FHD IPS USB-C Monitor",
            "description": "Dell U2422HE with built-in 90W USB-C hub that charges your MacBook or Windows laptop with a single cable! Super thin bezels, height adjustable & pivot stand. Zero dead pixels.",
            "price": 7200,
            "category": "electronics",
            "condition": "Good condition",
            "status": "active",
            "seller_id": marcus.id,
            "days_ago": 3,
            "images": [
                "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Apple Magic Keyboard 2 + Magic Mouse 2 Space Gray",
            "description": "Sleek Apple Bluetooth desktop accessories. Rechargeable via Lightning. Both in clean cosmetic condition with snappy key travel. Selling because I upgraded to mechanical keyboard.",
            "price": 4500,
            "category": "electronics",
            "condition": "Good condition",
            "status": "active",
            "seller_id": sarah.id,
            "days_ago": 6,
            "images": [
                "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80"
            ]
        },

        # Cycles
        {
            "title": "Trek FX 2 Disc Commuter Hybrid Bike (Medium)",
            "description": "Lightweight aluminum frame, Shimano 2x9 gearing, and hydraulic disc brakes for stopping power in all campus weather. Serviced last month at Campus Bike Shop. Includes Kryptonite U-lock and rear mudguard.",
            "price": 14000,
            "category": "cycles",
            "condition": "Good condition",
            "status": "active",
            "seller_id": marcus.id,
            "days_ago": 1,
            "images": [
                "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1532298229144-0ec0c57515c7?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Firefox Target 29T 21-Speed Mountain Bike",
            "description": "Front suspension fork with dual disc brakes, 29-inch wheels. Great for getting across campus quickly and gravel shortcut trails. Tuned up and ready to ride immediately.",
            "price": 8500,
            "category": "cycles",
            "condition": "Good condition",
            "status": "active",
            "seller_id": priya.id,
            "days_ago": 7,
            "images": [
                "https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?auto=format&fit=crop&w=800&q=80"
            ]
        },

        # Bags
        {
            "title": "The North Face Borealis 28L College Backpack",
            "description": "Classic college backpack with dedicated 15\" padded laptop sleeve, FlexVent suspension shoulder straps, and bungee front cords for jackets. Water-repellent finish, no rips or broken zippers.",
            "price": 2900,
            "category": "bags",
            "condition": "Like new",
            "status": "active",
            "seller_id": sarah.id,
            "days_ago": 3,
            "images": [
                "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Bellroy Classic 20L Water-Resistant Laptop Backpack",
            "description": "Minimalist premium charcoal backpack made from recycled woven fabric. Has internal iPad pocket, sunglasses pouch, and luminescent zipper pulls. Extremely comfortable for long lab days.",
            "price": 3600,
            "category": "bags",
            "condition": "Like new",
            "status": "active",
            "seller_id": alex.id,
            "days_ago": 9,
            "images": [
                "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?auto=format&fit=crop&w=800&q=80"
            ]
        },

        # Hostel Essentials
        {
            "title": "Philips 1.5L Stainless Steel Electric Kettle",
            "description": "Fast-boil 1800W cordless electric kettle. Food-grade stainless steel body with auto shut-off and boil-dry protection. A dorm room survival must-have for tea, instant noodles, and oats.",
            "price": 750,
            "category": "hostel",
            "condition": "Like new",
            "status": "active",
            "seller_id": sarah.id,
            "days_ago": 2,
            "images": [
                "https://images.unsplash.com/photo-1585837575652-267c041d77d4?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "IKEA Forså Classic Work Desk Lamp (Matte Black)",
            "description": "Adjustable arm and head so you can direct the light right onto your desk or textbook without disturbing roommates. Includes warm 2700K energy-efficient LED bulb.",
            "price": 600,
            "category": "hostel",
            "condition": "Good condition",
            "status": "active",
            "seller_id": priya.id,
            "days_ago": 4,
            "images": [
                "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Foldable Bed Study Table & Lap Desk with Slot",
            "description": "Heavy-duty engineered wood lap desk with cup holder and tablet slot. Folds flat to slide under bed or beside wardrobe. Perfect for late night assignments.",
            "price": 500,
            "category": "hostel",
            "condition": "Fair condition",
            "status": "active",
            "seller_id": alex.id,
            "days_ago": 12,
            "images": [
                "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=800&q=80"
            ]
        },
        # Add a Sold and a Draft item for Alex's dashboard stats per PRD Section 7.7
        {
            "title": "Anker 65W GaN USB-C Fast Charger",
            "description": "Sold during midterm week to a batchmate.",
            "price": 1200,
            "category": "electronics",
            "condition": "Like new",
            "status": "sold",
            "seller_id": alex.id,
            "days_ago": 15,
            "images": [
                "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=800&q=80"
            ]
        },
        {
            "title": "Sony Alpha A6000 Mirrorless Camera Body",
            "description": "Draft listing in progress for campus photography club gear.",
            "price": 18500,
            "category": "electronics",
            "condition": "Good condition",
            "status": "draft",
            "seller_id": alex.id,
            "days_ago": 1,
            "images": [
                "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80"
            ]
        }
    ]

    created_items = []
    for item_raw in items_data:
        imgs = item_raw.pop("images")
        days = item_raw.pop("days_ago")
        created_time = datetime.now(timezone.utc) - timedelta(days=days)
        sold_time = created_time + timedelta(days=2) if item_raw["status"] == "sold" else None

        it = Item(
            **item_raw,
            created_at=created_time,
            sold_at=sold_time
        )
        db.add(it)
        db.commit()
        db.refresh(it)

        for pos, img_url in enumerate(imgs):
            img = ItemImage(
                item_id=it.id,
                url=img_url,
                position=pos
            )
            db.add(img)
        db.commit()
        created_items.append(it)

    # 3. Wishlist entries for Alex
    # Alex saved: CLRS Book (id 3), Trek Hybrid Bike (id 8), Bellroy Backpack (id 11)
    wishlist_targets = [it for it in created_items if it.seller_id != alex.id and it.status == "active"]
    if len(wishlist_targets) >= 3:
        for t in wishlist_targets[:3]:
            w = WishlistEntry(user_id=alex.id, item_id=t.id)
            db.add(w)
        db.commit()

    # 4. Conversations & Messages
    # Conversation 1: Priya inquiring with Alex about the TI-84 Plus CE
    ti84_item = next((it for it in created_items if "TI-84" in it.title), created_items[0])
    conv1 = Conversation(
        item_id=ti84_item.id,
        buyer_id=priya.id,
        seller_id=alex.id,
        created_at=datetime.now(timezone.utc) - timedelta(hours=3)
    )
    db.add(conv1)
    db.commit()
    db.refresh(conv1)

    m1 = Message(
        conversation_id=conv1.id,
        sender_id=priya.id,
        text="Hey Alex! Is the TI-84 Plus CE calculator still available?",
        is_read=True,
        created_at=datetime.now(timezone.utc) - timedelta(hours=3)
    )
    m2 = Message(
        conversation_id=conv1.id,
        sender_id=alex.id,
        text="Hi Priya! Yes, still available and comes with the mini-USB charging cable and slide cover.",
        is_read=True,
        created_at=datetime.now(timezone.utc) - timedelta(hours=2, minutes=45)
    )
    m3 = Message(
        conversation_id=conv1.id,
        sender_id=priya.id,
        text="Awesome! Could we meet up at the Engineering Quad around 4:30 PM today?",
        is_read=False,
        created_at=datetime.now(timezone.utc) - timedelta(minutes=25)
    )
    db.add_all([m1, m2, m3])

    # Conversation 2: Marcus inquiring with Alex about the Sony Headphones
    sony_item = next((it for it in created_items if "Sony WH" in it.title), created_items[5])
    conv2 = Conversation(
        item_id=sony_item.id,
        buyer_id=marcus.id,
        seller_id=alex.id,
        created_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    db.add(conv2)
    db.commit()
    db.refresh(conv2)

    m4 = Message(
        conversation_id=conv2.id,
        sender_id=marcus.id,
        text="Hey, are the ear cushions in good condition? Any noticeable battery degradation?",
        is_read=True,
        created_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    m5 = Message(
        conversation_id=conv2.id,
        sender_id=alex.id,
        text="Hey Marcus, ear cushions were replaced last month and battery still holds ~28 hours with ANC on. Works like a charm!",
        is_read=True,
        created_at=datetime.now(timezone.utc) - timedelta(hours=22)
    )
    db.add_all([m4, m5])
    db.commit()

    print(f"Successfully seeded:")
    print(f"- {db.query(User).count()} Users")
    print(f"- {db.query(Item).count()} Items")
    print(f"- {db.query(ItemImage).count()} Images")
    print(f"- {db.query(WishlistEntry).count()} Wishlist items")
    print(f"- {db.query(Conversation).count()} Conversations")
    print(f"- {db.query(Message).count()} Messages")
    db.close()

if __name__ == "__main__":
    seed()
