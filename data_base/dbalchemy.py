from os import path
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base

from settings import config
from models.product import Products
from models.order import Order
from models.category import Category
from models.subcategory import Subcategory
from settings import utility


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сессии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_categories(self):
        result = self._session.query(Category).all()
        self.close()
        return result

    def select_subcategories(self, category):
        category_id = self._session.query(Category).filter(Category.name == category).first().id
        result = self._session.query(Subcategory).filter(Subcategory.category_id == category_id).all()
        self.close()
        return result

    def select_products(self, category, subcategory):
        products = self._session.query(Products).filter(Products.category_id == category).filter(Products.subcategory_id == subcategory).all()
        self.close()
        return products

    def get_category_id_from_name(self, category_name):
        category_id = self._session.query(Category).filter(Category.name == category_name).first().id
        self.close()
        return category_id

    def get_product(self, product_id):
        product = self._session.query(Products).filter(Products.id == product_id).first()
        self.close()
        return product

    def set_order(self, quantity, product_id, user_id):
        order = Order(quantity=quantity, product_id=product_id, user_id=user_id, data=datetime.now())
        self._session.add(order)
        self._session.commit()
        self.close()

    def get_orders_by_user_id(self, user_id):
        orders = self._session.query(Order).filter(Order.user_id == user_id).all()
        self.close()
        return orders


    def close(self):
        """ Закрывает сесию """
        self._session.close()