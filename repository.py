from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from createDb import Base, Category, Item

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
database_session = sessionmaker(bind=engine)
session = database_session()

class Repository:
    def getAllItems(self):
        return session.query(Item).all()

    def getItemById(self, item_id):
        return session.query(Item).get(item_id)

    def addItemToDatabase(self, name, description, categoryid):
        item = Item(name=name, description=description, categoryid=categoryid)
        session.add(item)
        session.commit()
        return

    def addToDatabase(self, new_or_updated_object):
        session.add(new_or_updated_object)
        session.commit()
        return

    def deleteFromDatabase(self, item):
        session.delete(item)
        session.commit()
        return

    def deleteAllFromDatabase(self):
        session.query(Item).delete()
        session.commit()
        session.query(Category).delete()
        session.commit()
        return