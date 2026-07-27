from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Boolean,Float
from sqlalchemy import func

#подклюбчение к бд и создание сессии
Base = declarative_base()
engine = create_engine('sqlite:///shop.db')
Session = sessionmaker(bind=engine)
session = Session()

#создание классов под таблицу
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    description = Column(String)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="products")

Base.metadata.create_all(engine)

#заполнение классов
# electronics = Category(name="Электроника", description="Гаджеты и устройства.")
# books = Category(name="Книги", description="Печатные книги и электронные книги.")
# clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")
#
# #session.add_all([electronics, books, clothes])
# #session.commit()
#
# smartphone = Product(name="Смартфон", price=299.99, in_stock=True, category=electronics)
# laptop = Product(name="Ноутбук", price=499.99, in_stock=True, category=electronics)
# novel = Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=books)
# jeans = Product(name="Джинсы", price=40.50, in_stock=True, category=clothes)
# tshirt = Product(name="Футболка", price=20.00, in_stock=True, category=clothes)
#
# session.add_all([smartphone, laptop, novel, jeans, tshirt])
# session.commit()

#task 2
categories = session.query(Category).all()

for category in categories:
    print(f"Категория: {category.name}")
    for product in category.products:
        print(f"     {product.name}: {product.price}")


#task 3
smartphone = session.query(Product).filter_by(name='Смартфон').first()
smartphone.price = 349.99
session.commit()

#task 4
agr = session.query(Category.name,func.count(Product.id)).join(Product).group_by(Category.name).all()
for name, count in agr:
    print(f"{name}: {count} продуктов")

#task5
new_agr = (
    session.query(Category.name, func.count(Product.id))
    .join(Product)
    .group_by(Category.name)
    .having(func.count(Product.id) > 1)
    .all()
)
