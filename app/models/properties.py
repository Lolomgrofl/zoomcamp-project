from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, intpk


class Property(Base):
    __tablename__ = "properties"
    propertyid: Mapped[intpk]
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    zipcode: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[float | None]
    bedrooms: Mapped[int | None]
    bathrooms: Mapped[int | None]
    squarefeet: Mapped[int | None]
    geometry: Mapped[str] = mapped_column(String(255), nullable=False)
