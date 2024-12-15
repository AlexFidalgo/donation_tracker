from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

# Define the database URL
DATABASE_URL = "sqlite:///donations.db"  # SQLite database file

# Set up the database engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for ORM models
Base = declarative_base()

# Define the Donations table
class DonationEntry(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_date = Column(DateTime, default=lambda: datetime.utcnow().replace(tzinfo=pytz.utc))
    total_arrecadado = Column(String, nullable=False)
    percent_meta = Column(Float, nullable=False)

# Create the table in the database
Base.metadata.create_all(bind=engine)
