import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_role = Column(Integer, ForeignKey('roles.id'), nullable=False)
    name = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(128))
    created_at = Column(TIMESTAMP(), default=datetime.now())
    updated_at = Column(TIMESTAMP(), default=datetime.now(),
                        onupdate=datetime.now())
    is_banned = Column(Boolean, default=False)

    role = relationship('Role', backref='users')
    orders = relationship('Order', backref='user')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Cambio aquí de id_user a user_id
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    price = Column(Float)
    created_at = Column(TIMESTAMP(), default=datetime.now())

    products = relationship('OrderProduct', back_populates='order')



class OrderProduct(Base):
    __tablename__ = 'orders_products'
    id_order = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    id_product = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    order = relationship('Order', back_populates='products')


class Database:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def list_orders(self):
        return self.session.query(Order).all()

    def add_order(self, order):
        self.session.add(order)
        self.session.commit()
        return order

    def add_order_products(self, order_id, product_id, quantity):
        order_product = OrderProduct(
            id_order=order_id, id_product=product_id, quantity=quantity)
        self.session.add(order_product)
        self.session.commit()
        return True

    def get_order(self, order_id):
        return self.session.query(Order).filter(Order.id == order_id).one_or_none()

    def delete_order(self, order_id):
        order = self.get_order(order_id)
        if order:
            self.session.delete(order)
            self.session.commit()
            return True
        return False
