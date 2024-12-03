from sqlalchemy import Column, Integer, String
from database.vin import VIN

from database.database import Base

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    vin = Column(VIN, unique=True)
    manufacturer_name = Column(String)
    model_name = Column(String)
    model_year = Column(Integer)
    fuel_type = Column(String)
    purchase_price = Column(Integer)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
