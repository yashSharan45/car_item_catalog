from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Car, Base, Item, User

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Menu for BMW
car1 = Car(user_id=1, name="BMW")

session.add(car1)
session.commit()

mi2 = Item(user_id=1, name=" X6 ", description="A heavy duty SUV with multipurpose uses",
                     price="Rs 1.2 Cr", course="Entree", restaurant=car1)

session.add(mi2)
session.commit()


mi1 = Item(user_id=1, name="i8", description="A sports car with 200 km\hr speed and 0-100 in 6 sec",
                     price="Rs 2.14 Cr", course="Appetizer", restaurant=car1)

session.add(mi1)
session.commit()


mi3 = Item(user_id=1, name="GT", description="Luxury car with automatic gear transmission and comes in 3 varient",
                     price="Rs 56.48 Lakh", course="Dessert", restaurant=car1)

session.add(mi3)
session.commit()


# Menu for AUDI
car2 = Car(user_id=1, name="AUDI")

session.add(car2)
session.commit()

mi2 = Item(user_id=1, name=" Q7 ", description="A heavy duty SUV with multipurpose uses",
                     price="Rs 90 Lakh", course="Entree", restaurant=car2)

session.add(mi2)
session.commit()


mi1 = Item(user_id=1, name="R8", description="A sports car with 200 km\hr speed and 0-100 in 4 sec",
                     price="Rs 2.44 Cr", course="Appetizer", restaurant=car2)

session.add(mi1)
session.commit()


mi3 = Item(user_id=1, name="A6", description="Luxury car with automatic gear transmission and comes in 2 varient",
                     price="Rs 66.48 Lakh", course="Dessert", restaurant=car2)

session.add(mi3)
session.commit()


# Menu for Chevrolet
car3 = Car(user_id=1, name="Chevrolet")

session.add(car3)
session.commit()

mi2 = Item(user_id=1, name=" Suburban ", description="A heavy duty SUV with multipurpose uses and can be use for offroadings",
                     price="Rs 2.2Cr", course="Entree", restaurant=car3)

session.add(mi2)
session.commit()


mi1 = Item(user_id=1, name="Camaro", description="a semi sports and muscle car with graet built",
                     price="Rs 50 Lakh", course="Appetizer", restaurant=car3)

session.add(mi1)
session.commit()


mi3 = Item(user_id=1, name="Cruze", description="Luxury car with automatic gear transmission and alose comes in disel varient too with bit heigher range",
                     price="Rs 56.48Lakh", course="Dessert", restaurant=car3)

session.add(mi3)
session.commit()


# Menu for Jaguar
car4 = Car(user_id=1, name="Jaguar")

session.add(car4)
session.commit()

mi2 = Item(user_id=1, name=" F-Pace ", description="A heavy duty SUV that can be used for offroadings",
                     price="Rs 1.7 Cr", course="Entree", restaurant=car4)

session.add(mi2)
session.commit()


mi1 = Item(user_id=1, name="XE", description="A fast car with luxury and top speed of 250 km/hr",
                     price="Rs 50 Lakh", course="Appetizer", restaurant=car4)

session.add(mi1)
session.commit()


mi3 = Item(user_id=1, name="XF", description="A long sydane with lots of space and comfort",
                     price="Rs 48.48Lakh", course="Dessert", restaurant=car4)

session.add(mi3)
session.commit()


# Menu for Renault
car5 = Car(user_id=1, name="Renault")

session.add(car5)
session.commit()

mi2 = Item(user_id=1, name=" Duster ", description="A mid range suv witj lots of functionality",
                     price="Rs 10 lakh", course="Entree", restaurant=car5)

session.add(mi2)
session.commit()


mi1 = Item(user_id=1, name="RS", description="a sports with 2000hp and suoer quick ignetion and high pickup",
                     price="Rs 3 Cr", course="Appetizer", restaurant=car5)

session.add(mi1)
session.commit()


mi3 = Item(user_id=1, name="Scala", description="Luxury car with automatic gear transmission",
                     price="Rs 15 Lakh", course="Dessert", restaurant=car5)

session.add(mi3)
session.commit()


print "added menu items!"
