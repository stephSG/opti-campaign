from app.database import engine, Base
from app.models import Campaign  # We must import all models here

print("Connecting to database and creating tables...")

# This line reads the 'metadata' from our Base (which Campaign belongs to)
# and creates all corresponding tables in the database defined by 'engine'.
try:
    Base.metadata.create_all(bind=engine)
    print(f"Successfully created tables in the database.")
    print(f"Database file should be located at: 'backend/sql_app.db'")

except Exception as e:
    print(f"An error occurred while creating tables: {e}")
