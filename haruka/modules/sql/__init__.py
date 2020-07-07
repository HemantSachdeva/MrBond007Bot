from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from haruka import DB_URI
DB_URI='postgres://nokdsleh:SyVHLt2bdPXDJ1apb6M129Sr2H8XPBvq@ruby.db.elephantsql.com:5432/nokdsleh'

def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    #engine = create_engine(os.environ.get(DB_URI,str))
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()