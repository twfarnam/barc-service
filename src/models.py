import os
import json
import datetime
from PIL import Image as PILImage
from sqlalchemy import create_engine, inspect, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import uuid4

db_path = os.path.normpath(os.path.dirname(__file__) + '/../barc.db')

engine = create_engine('sqlite:///' + db_path, echo=True)

Base = declarative_base()

def newID():
    return str(uuid4())

def now():
    return datetime.datetime.now().isoformat()

def width(context):
    id = context.get_current_parameters()['id']
    filename = os.path.join(Image.DIR, id + '.jpg')
    img = PILImage.open(filename)
    return img.size[0]

def height(context):
    id = context.get_current_parameters()['id']
    filename = os.path.join(Image.DIR, id + '.jpg')
    img = PILImage.open(filename)
    return img.size[1]


images_categories_table = Table(
    'images_categories',
    Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Image(Base):
    __tablename__ = 'images'

    DIR = os.path.normpath(os.path.dirname(__file__) + '/../images')

    id = Column(String, primary_key=True, default=newID)
    width = Column(Integer, nullable=False, default=width)
    height = Column(Integer, nullable=False, default=height)
    created_at = Column(String, nullable=False, index=True, default=now)
    result = Column(String)
    motion = Column(String)
    device_id = Column(String)
    ip_address = Column(String)
    categories = relationship("Category", secondary=images_categories_table)

    def dict(self):
        attrs = inspect(self).mapper.column_attrs
        image = { c.key: getattr(self, c.key) for c in attrs }
        image['categories'] = [ c.id for c in self.categories ]
        if self.result: image['result'] = json.loads(self.result)
        if self.motion: image['motion'] = json.loads(self.motion)
        return image

    def filename(self):
        return os.path.join(Image.DIR, self.id + '.jpg')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True, default=newID)
    room = Column(String, nullable=False)
    object = Column(String, nullable=False)

    @hybrid_property
    def label(self):
        return self.room + ' | ' + self.object

    def dict(self):
        attrs = inspect(self).mapper.column_attrs
        return { c.key: getattr(self, c.key) for c in attrs }


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

