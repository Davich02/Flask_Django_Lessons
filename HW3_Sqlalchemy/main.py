from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# creating a connection to the database
engine = create_engine('sqlite:///:memory:')
# creating a session
Session = sessionmaker(bind=engine)
# creating an object for the session
session = Session()

# creating a class for the table
class Base(DeclarativeBase):
    pass

# creating a class for product table
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10,2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('categories.id'))

# creating a class for category table
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(255))


