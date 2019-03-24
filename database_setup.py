import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    photo = Column(String(255))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User, backref="category")

    @property
    def serialize(self):
        # Convert a Category object into a dictionary
        return {
            'id': self.id,
            'title': self.title,
        }


class CategoryItem(Base):
    __tablename__ = 'category_items'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    title = Column(String(255), nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship(Category, backref="category_items")

    @property
    def serialize(self):
        # Convert a Category object into a dictionary
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id,
            'category_title': self.category.title
        }

if __name__ == "__main__":
    DATABASE = 'postgresql://linux:linux@127.0.0.1:5432/catalog'
    engine = create_engine(DATABASE)
    Base.metadata.create_all(engine)
