from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session
from model import Base


class Contragent(Base):
    __tablename__ = 'contragents'

    ipn = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    phone_number = Column(String(15), nullable=False)

    def __str__(self):
        return f"Contragent [ipn={self.ipn}, name={self.name}, phone_number={self.phone_number}]"

    @staticmethod
    def get_distinct_names(session: Session):
        return [name for (name,) in session.query(Contragent.name).all()]
