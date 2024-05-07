import os
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=sqlalchemy.func.now())
    pedido_producto_id = Column(Integer)
    id_pedido = Column(Integer)
    id_producto = Column(Integer)
    cantidad = Column(Integer)

class Database:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL')) 
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def list_orders(self):
        return self.session.query(Order).all()

    def add_order(self, id_usuario, pedido_producto_id, id_pedido, id_producto, cantidad):
        new_order = Order(id_usuario=id_usuario, pedido_producto_id=pedido_producto_id, id_pedido=id_pedido, id_producto=id_producto, cantidad=cantidad)
        self.session.add(new_order)
        self.session.commit()
        return True



