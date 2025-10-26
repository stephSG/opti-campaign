from app.database import engine, Base, SessionLocal
from app.models import User, Campaign  # We must import all models here
from app.schemas import UserCreate, CampaignCreate
from app.crud import get_user_by_username, create_user, create_campaign
from datetime import date

print("Connecting to database and creating tables...")

# This line reads the 'metadata' from our Base (which Campaign belongs to)
# and creates all corresponding tables in the database defined by 'engine'.
try:
    Base.metadata.create_all(bind=engine)
    print(f"Successfully created tables in the database.")
    print(f"Database file should be located at: 'backend/sql_app.db'")

except Exception as e:
    print(f"An error occurred while creating tables: {e}")
    exit()

# Create a new database session
db = SessionLocal()

# --- Create Initial User ---
# Check if the user already exists
user = get_user_by_username(db, username="admin")
if not user:
    print("Creating initial user 'admin'...")
    user_in = UserCreate(username="admin", password="password")
    create_user(db=db, user=user_in)
    print("User 'admin' created successfully.")
else:
    print("User 'admin' already exists.")


# --- Create Initial Campaigns ---
# We check if campaigns already exist to avoid duplicates.
# A simple check on the first campaign name is sufficient for this seed script.
from app.crud import get_campaigns
if not any(c.name == "Summer Sale 2025" for c in get_campaigns(db)):
    print("Creating initial campaigns...")
    campaigns_to_create = [
        CampaignCreate(
            name="Summer Sale 2025",
            description="A hot summer sale campaign.",
            start_date=date(2025, 6, 1),
            end_date=date(2025, 8, 31),
            budget=5000.00,
            status=True,
        ),
        CampaignCreate(
            name="Black Friday Deals",
            description="Biggest sale of the year.",
            start_date=date(2025, 11, 20),
            end_date=date(2025, 11, 30),
            budget=15000.00,
            status=True,
        ),
    ]

    for campaign_in in campaigns_to_create:
        create_campaign(db=db, campaign=campaign_in)

    print(f"{len(campaigns_to_create)} campaigns created successfully.")
else:
    print("Initial campaigns already exist.")


# Close the session
db.close()
print("Database initialization finished.")
