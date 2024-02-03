from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass


class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(55), unique=False, nullable=False)
    tag: Mapped[str] = mapped_column(String(50), nullable=False)
    expiration_date: Mapped[str] = mapped_column(DateTime, nullable=False)
    additional_info: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'Inventory(id={self.id!r}, item_name={self.item_name!r}, tag={self.tag!r}, expiration_date={self.expiration_date!r}, additional_info={self.additional_info!r})'
