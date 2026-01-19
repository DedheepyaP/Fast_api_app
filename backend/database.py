from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


#db_url = "postgresql+psycopg2://dedheepya:postgres@localhost:5432/mydb"

db_url = "postgresql://dedheepya:postgres@db:5432/mydb"

engine = create_engine(
    db_url,
    pool_pre_ping=True
)

# engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# session = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()