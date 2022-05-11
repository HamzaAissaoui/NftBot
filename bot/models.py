from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from helper import logger
from config.settings import Settings

Base = declarative_base()
'''Comments before every execution'''
@event.listens_for(Engine, "before_cursor_execute")
def comment_sql_calls(conn, cursor, statement, parameters,
                                    context, executemany):
    logger.warning(statement)

'''Creating an engine'''
engine = create_engine(     
                        f"""
                        {Settings.get_db_ORDBMS()}+{Settings.get_db_interpreter()}://\
                        {Settings.get_db_user()}:{Settings.get_db_password()}@\
                        {Settings.get_db_host()}:{Settings.get_db_port()}/\
                        {Settings.get_db_name()}
                        """, echo=False, future=True
                    )

db = Session(engine)

class Sneaker(Base):
    __tablename__ = 'sneaker'
    id = Column(Integer, primary_key=True)
    sneaker_id = Column(String(40))
    efficiency = Column(Float(3))
    luck = Column(Float(3))
    resilience = Column(Float(3))
    attributes_sum = Column(Float(4))
    price = Column(Float(5))
    def __repr__(self):
       return f"Sneaker(id={self.id!r}, sneaker_id={self.sneaker_id!r}, efficiency={self.efficiency!r}, luck={self.luck!r}, resilience={self.resilience!r},\
           attributes_sum={self.attributes_sum!r}, price={self.price!r})"


class Attributes(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True)
    min_attribute_sum = Column(Float(3))
    max_attribute_sum = Column(Float(3))
    total_sneakers = Column(Integer)
    cheapest_average_price = Column(Float(5)) #of the 10 cheapest sneakers in this interval
    def __repr__(self):
        return f"Attributes(id={self.id!r}, min_attribute_sum={self.min_attribute_sum!r}, max_attribute_sum={self.max_attribute_sum!r}, total_sneakers={self.total_sneakers!r},\
            cheapest_average_price={self.cheapest_average_price!r})"


class BoughtSneaker(Base):
    __tablename__ = 'bought_sneaker'
    id = Column(Integer, primary_key=True)
    sneaker_id = Column(String(40))
    buying_price = Column(Float(5))
    selling_price = Column(Float(5))
    def __repr__(self):
       return f"BoughtSneaker(id={self.id!r}, sneaker_id={self.sneaker_id!r}, buying_price={self.buying_price!r}, selling_price={self.selling_price!r})"    


class ScrappingStatus(Base):
    __tablename__ = 'scrapping_status'
    id = Column(Integer, primary_key=True)
    last_scrapped = Column(DateTime)
    finished_scrapping = Column(Boolean)
    def __repr__(self):
       return f"ScrappingStatus(id={self.id!r}, last_scrapped={self.last_scrapped!r}, finished_scrapping={self.finished_scrapping!r})"    

    

def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)

def fill_attributes_table():
    min_ = 0.1
    max_ = 1
    with db as session:
        while max_ <= 30:
            attribute = Attributes(min_attribute_sum=min_, max_attribute_sum=max_, total_sneakers=0, cheapest_average_price=0)
            session.add(attribute)
            session.commit()
            min_+=1
            max_+=1
    
def get_attributes_ids():
    with db as session:
        for row in session.scalars(select(Attributes).filter_by(id=1)):
                print(row) 
            
def fill_scrapping_status():
    with db as session:
        attribute = ScrappingStatus(last_scrapped=datetime.now(), finished_scrapping=False)
        session.add(attribute)
        session.commit()

        
