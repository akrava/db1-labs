from sqlalchemy import Column, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from model import Base


class Reweightings(Base):
    __tablename__ = 'reweightings'

    id = Column(Integer, primary_key=True)
    weight_before = Column(Integer, nullable=False)
    weight_after = Column(Integer, nullable=False)
    date_inspection = Column(DateTime, nullable=False)
    parcel_id = Column(Integer, ForeignKey('goods.id', onupdate='restrict', ondelete='restrict'), nullable=False)

    parcel = relationship("Goods", backref="reweightings")

    __table_args__ = (
        Index(
            'date_inspection_index',
            date_inspection,
            postgresql_using='brin'
        ),
    )

    def __str__(self):
        return f"Reweightings [id={self.id}, weight_before={self.weight_before}, weight_after={self.weight_after}, " \
               f"date_inspection={self.date_inspection}, parcel_id={self.parcel_id}]"
