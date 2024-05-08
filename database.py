import os
from sqlalchemy import create_engine, Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import sqlalchemy

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=sqlalchemy.func.now())

    products = relationship("OrderProduct", back_populates="order")

class OrderProduct(Base):
    __tablename__ = 'orders_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="products")

class Database:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL')) 
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def list_orders(self):
        return self.session.query(Order).all()

    def add_order(self, id_usuario, id_pedido, id_producto, cantidad):
        new_order = Order(id_usuario=id_usuario, id_pedido=id_pedido, id_producto=id_producto, cantidad=cantidad)
        self.session.add(new_order)
        self.session.commit()
        return True

    def list_order_products(self):
        return self.session.query(OrderProduct).all()
    
    def add_order_products(self, order_id, product_id, quantity):
        new_order_product = OrderProduct(order_id=order_id, product_id=product_id, quantity=quantity)
        self.session.add(new_order_product)
        self.session.commit()
        return True
