import os
from databases import Database
import sqlalchemy

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/reporting"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

product_events = sqlalchemy.Table(
    "product_events",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("evt_type", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("product_id", sqlalchemy.String),
    sqlalchemy.Column("location_id", sqlalchemy.String),
    sqlalchemy.Column("location", sqlalchemy.String),
    sqlalchemy.Column("evt_date", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("transaction_id", sqlalchemy.String),
    sqlalchemy.Column("platform", sqlalchemy.String),
    sqlalchemy.Column("meta", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("created", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("last_modified", sqlalchemy.TIMESTAMP),
)

user_events = sqlalchemy.Table(
    "user_events",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("evt_type", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("evt_date", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("platform", sqlalchemy.String),
    sqlalchemy.Column("meta", sqlalchemy.String),
    sqlalchemy.Column("created", sqlalchemy.TIMESTAMP),
    sqlalchemy.Column("last_modified", sqlalchemy.TIMESTAMP),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

