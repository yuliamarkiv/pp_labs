from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


# engine = create_engine("mysql://root:123abc!!!@127.0.0.1:3306/adservice", paramstyle='format', echo=True)
engine = create_engine("mysql+pymysql://root:password@127.0.0.1:3306/adservice")
# , paramstyle='format', echo=True
Base = declarative_base()


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return f"location:\n" \
               f"id={self.id}\n" \
               f"name={self.name}"


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    locationId = Column(Integer, ForeignKey('location.id'), nullable=False)

    location = relationship(Location, backref='user', lazy=False)

    def __str__(self):
        return f"user:\n" \
               f"id={self.id}\n" \
               f"name={self.username}\n" \
               f"email={self.email}\n" \
               f"password={self.password}\n" \
               f"locationId={self.locationId}"


class Ad(Base):
    __tablename__ = 'ad'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    text = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)
    locationId = Column(Integer, ForeignKey('location.id'), nullable=True)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)

    location = relationship(Location, backref='ad', lazy=False)
    user = relationship(User, backref='ad', lazy=False)

    def __str__(self):
        return f"ad:\n" \
               f"id={self.id}\n" \
               f"name={self.name}\n" \
               f"text={self.text}\n" \
               f"price={self.price}\n" \
               f"currency={self.currency}\n" \
               f"date={self.date}\n" \
               f"locationId={self.locationId}\n" \
               f"userId={self.userId}"
