# class Base(DeclarativeBase):
#     pass


# class InventoryItem(Base):
#     __tablename__ = 'inventory'

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     item_name: Mapped[str] = mapped_column(String(55), unique=False, nullable=False)
#     category: Mapped[str] = mapped_column(String(50), nullable=False)
#     expiration_date: Mapped[str] = mapped_column(DateTime, nullable=False)
#     additional_info: Mapped[str] = mapped_column(String(255), nullable=False)

#     def __repr__(self):
#         return f'InventoryItem(id={self.id!r}, item_name={self.item_name!r}, category={self.category!r}, expiration_date={self.expiration_date!r}, additional_info={self.additional_info!r})'


# class Category(Base):
#     __tablename__ = 'categories'

#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     category: Mapped[str] = mapped_column(String(50), nullable=False)

#     def __repr__(self):
#         return f'Category(id={self.id!r}, item_name={self.category})'
