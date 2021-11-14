from sqlalchemy.orm import sessionmaker
from models import *

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# location_1 = Location(name='Lviv')
# session.add(location_1)
# location_2 = Location(name='Kyiv')
# session.add(location_2)
# user1 = User(username='Andrii', email='somemail@gmail.com', password='12345', location=location_1)
# session.add(user1)
# ad1 = Ad(name='Sell boots', text='Mustang boots with warm fur inside, size 43, manufacturer Portugal',
#          price='123.56', currency='USD', date='2019-05-17', location=location_1, user=user1)
# session.add(ad1)
# session.commit()
#
# locations = session.query(Location).all()
# users = session.query(User).all()
# ads = session.query(Ad).all()
# for location in locations:
#     print('\n', location)
#
# for user in users:
#     print('\n', user)
# for ad in ads:
#     print('\n', ad)
