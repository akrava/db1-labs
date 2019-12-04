from sqlalchemy import Column, Integer, ForeignKey, Date, DECIMAL, func, Index
from sqlalchemy.orm import Session, relationship
from model import Base


class Invoice(Base):
    __tablename__ = 'invoices'

    num = Column(Integer, primary_key=True)
    date_departure = Column(Date, nullable=False)
    date_arrival = Column(Date)
    shipping_cost = Column(DECIMAL, nullable=False)
    sender_ipn = \
        Column(Integer, ForeignKey('contragents.ipn', onupdate='restrict', ondelete='restrict'), nullable=False)
    recipient_ipn = \
        Column(Integer, ForeignKey('contragents.ipn', onupdate='restrict', ondelete='restrict'), nullable=False)
    warehouse_dep_num = \
        Column(Integer, ForeignKey('warehouses.num', onupdate='restrict', ondelete='restrict'), nullable=False)
    warehouse_arr_num = \
        Column(Integer, ForeignKey('warehouses.num', onupdate='restrict', ondelete='restrict'), nullable=False)

    sender = relationship("Contragent", backref="invoices_outbox", foreign_keys=[sender_ipn])
    recipient = relationship("Contragent", backref="invoices_inbox", foreign_keys=[recipient_ipn])
    warehouse_arrival = relationship("Warehouse", backref="invoices_arriving", foreign_keys=[warehouse_arr_num])
    warehouse_departure = relationship("Warehouse", backref="invoices_departing", foreign_keys=[warehouse_dep_num])

    __table_args__ = (
        Index(
            'sender_ipn_index',
            sender_ipn,
            postgresql_using='btree'
        ),
        Index(
            'shipping_cost_index',
            shipping_cost,
            postgresql_using='brin'
        ),
    )

    def __str__(self):
        return f"Invoice [num={self.num}, date_departure={self.date_departure}, date_arrival={self.date_arrival}, " \
               f"shipping_cost={self.shipping_cost}, sender_ipn={self.sender_ipn}, " \
               f"recipient_ipn={self.recipient_ipn}, warehouse_dep_num={self.warehouse_dep_num}, " \
               f"warehouse_arr_num={self.warehouse_arr_num}]"

    @staticmethod
    def get_extremum_shipping_cost(session: Session):
        min_query = func.min(Invoice.shipping_cost)
        max_query = func.max(Invoice.shipping_cost)
        return session.query(min_query).scalar(), session.query(max_query).scalar()
