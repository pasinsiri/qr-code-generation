"""
Database initialization script for deployment.
Checks if the 'qrs' table exists in SQLite and creates it if not.
"""
import os
import sys
from sqlalchemy import create_engine, inspect
from app.database import SYNC_DATABASE_URL, metadata
from app.models import qrs


def init_database():
    """
    Initialize the database by creating the qrs table if it doesn't exist.
    """
    try:
        # Create engine
        engine = create_engine(SYNC_DATABASE_URL)

        # Create inspector to check existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        print(f"Database URL: {SYNC_DATABASE_URL}")
        print(f"Existing tables: {existing_tables}")

        # Check if 'qrs' table exists
        if 'qrs' not in existing_tables:
            print("Table 'qrs' not found. Creating table...")
            metadata.create_all(engine)
            print("✓ Table 'qrs' created successfully!")
        else:
            print("✓ Table 'qrs' already exists. No action needed.")

        # Verify the table was created/exists
        inspector = inspect(engine)
        if 'qrs' in inspector.get_table_names():
            columns = inspector.get_columns('qrs')
            print(f"✓ Verified table 'qrs' with {len(columns)} columns:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            return True
        else:
            print("✗ Failed to verify table creation")
            return False

    except Exception as e:
        print(f"✗ Error during database initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("Starting database initialization...")
    success = init_database()
    if success:
        print("\nDatabase initialization completed successfully!")
        sys.exit(0)
    else:
        print("\nDatabase initialization failed!")
        sys.exit(1)
