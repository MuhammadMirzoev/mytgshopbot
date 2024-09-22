# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from data_base.dbcore import Base

from models.category import Category
from sqlalchemy.orm import relationship, backref


class Subcategory(Base):
    """
    Класс-модель для описания таблицы "Подкатегория товара",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'subcategory'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    is_active = Column(Boolean)

    category = relationship(
        Category,
        backref=backref('subcategory',
                        uselist=True,
                        cascade='delete,all'))

    def __repr__(self):
        """
        Метод возвращает формальное строковое представление указанного объекта
        """
        return self.name
