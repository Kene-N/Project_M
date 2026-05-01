from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Renamed to mvp.db as requested
DATABASE_URL = "sqlite:///mvp.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✓ Local SQLite Database Initialized: mvp.db created.")

if __name__ == "__main__":
    init_db()