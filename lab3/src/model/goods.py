from sqlalchemy import Column, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from model import Base


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer, primary_key=True)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    description = Column(Text)
    invoice_num = Column(Integer, ForeignKey('invoices.num', onupdate='restrict', ondelete='restrict'), nullable=False)

    invoice = relationship("Invoice", backref="goods")

    __table_args__ = (
        Index(
            'goods_descriptions_index',
            func.to_tsvector('english', description),
            postgresql_using='gin'
        ),
        Index(
            'volume_index',
            height, width, depth,
            postgresql_using='brin'
        ),
        Index(
            'invoice_num_index',
            invoice_num,
            postgresql_using='btree'
        ),
    )

    def __str__(self):
        return f"Goods [id={self.id}, height={self.height}, width={self.width}, depth={self.depth}, " \
               f"weight={self.weight}, description={self.description}, invoice_num={self.invoice_num}]"
