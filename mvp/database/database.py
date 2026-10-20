from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Import the Base and the Metadata model specifically for the version check
from .models import Base, SystemMetadata 

DATABASE_URL = "sqlite:///mvp.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # This creates all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check for Version Tracker record
        version_entry = db.query(SystemMetadata).first()
        if not version_entry:
            # First time setup: Stamp the database as Version 1.0.0
            new_version = SystemMetadata(version="1.0.0")
            db.add(new_version)
            db.commit()
            print("✓ System Metadata: Version 1.0.0 Initialized.")
        else:
            print(f"✓ Running MVP Database v{version_entry.version}")
    except Exception as e:
        print(f"Version check failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()