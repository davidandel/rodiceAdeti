from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker

Base = declarative_base()
fake = Faker('cs_CZ')

class Rodic(Base):
    __tablename__ = 'rodic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    deti = relationship('Dite', back_populates='rodic', cascade='all, delete-orphan')

class Dite(Base):
    __tablename__ = 'dite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String, nullable=False)
    datum_narozeni = Column(String, nullable=False)
    rodic_id = Column(Integer, ForeignKey('rodic.id'), nullable=False)
    rodic = relationship('Rodic', back_populates='deti')

# Example usage
if __name__ == "__main__":
    engine = create_engine('sqlite:///rodic.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Add 20 random records
    for _ in range(20):
        novy_rodic = Rodic(jmeno=fake.first_name(), prijmeni=fake.last_name())
        nove_dite = Dite(jmeno=fake.first_name(), datum_narozeni=fake.date_of_birth().strftime('%Y-%m-%d'), rodic=novy_rodic)
        session.add(novy_rodic)
        session.add(nove_dite)

    session.commit()

    # Delete parent with id 8
    rodic_to_delete = session.query(Rodic).get(8)
    if rodic_to_delete:
        session.delete(rodic_to_delete)
        session.commit()

        # Display all parents and their children
    rodice = session.query(Rodic).all()
    for rodic in rodice:
        print(f'Rodic: {rodic.jmeno} {rodic.prijmeni}')
        for dite in rodic.deti:
            print(f'  Dite: {dite.jmeno}, Datum narozeni: {dite.datum_narozeni}')

    # Display parents and their children using left join
    results = session.query(Rodic).outerjoin(Dite).all()
    for rodic in results:
        print(f'Rodic: {rodic.jmeno} {rodic.prijmeni}')
        for dite in rodic.deti:
            print(f'  Dite: {dite.jmeno}, Datum narozeni: {dite.datum_narozeni}')
        if not rodic.deti:
            print('  Dite: None')