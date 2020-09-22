import os, sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# define a class whose instances you want to store with sql
class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    fidelity_credit = Column(Integer, primary_key=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"  # f-strings work from python 3.6 on
    
    def __repr__(self):
        return "Member('{}', '{}')".format(self.first_name, self.last_name)
    
    @classmethod
    def find_by_firstname(cls, session, first_name):
        return session.query(cls).filter_by(first_name=first_name).all()

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    member_id = Column(Integer, ForeignKey('member.id'))
    member = relationship(Member)

    def __repr__(self):
        return f"Address('{self.street_name}', '{self.street_number}', '{self.post_code}', '{self.member.full_name}')"


# set up a in-memory-only SQLite database
# echo sets up SQLAlchemy logging
engine = create_engine('sqlite:///:memory:', echo=False)

# Create all tables in the engine. 
# This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# Insert a Member in the member table
def add_member(m):
    session.add(m)
    session.commit()

memb1 = Member(first_name='Mack', last_name='Dean', fidelity_credit=10)
add_member(memb1)
 
# Insert an Address in the address table
def add_adress(addr):
    session.add(addr)
    session.commit()

addr1 = Address(post_code='12345', member=memb1)
add_adress(addr1)

""" Make queries in the members table """
# Make a query to find all Members in the database
session.query(Member).all()
# Return the first Member from all Members in the database
member = session.query(Member).first()
print(member.first_name)

# Find all Members whose member first_name field is 'Mack'
Member.find_by_firstname(session, 'Mack')
# this is the same as using the following:
session.query(Member).filter(Member.first_name=='Mack').first()
# find all Members with first_names similar to 'Mack'
session.query(Member).filter(Member.first_name.like('%Mack%')).first()


""" Make queries in the address table """
# Find all Address whose member field is pointing to the member object
session.query(Address).filter(Address.member == member).all()

# Retrieve one Address whose member field is point to the member object
session.query(Address).filter(Address.member == member).one()
address = session.query(Address).filter(Address.member == member).one()
print(address.post_code)


""" Create a new table after the initial create_all """
# create a new class
class Contract(Base):
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    member_id = Column(Integer, ForeignKey('member.id'))
    member = relationship(Member)

# create a new table
Contract.__table__.create(engine)

