from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True) # Идентификатор посылки
    name = Column(String(100), nullable=False) # Название посылки
    weight = Column(Float, nullable=False)  # Вес в кг
    content_cost = Column(Float, nullable=False)  # Стоимость содержимого в долларах
    delivery_cost = Column(Float, nullable=True)  # Стоимость доставки в рублях
    package_type_id = Column(Integer, ForeignKey("package_types.id"), nullable=False) # Идентификатор типа посылки
    session_id = Column(String(100), nullable=False)  # Идентификатор сессии пользователя

    package_type = relationship("PackageType")

    def __repr__(self):
        return f"<Package(id={self.id}, name={self.name}, weight={self.weight}, content_cost={self.content_cost}, delivery_cost={self.delivery_cost})>"