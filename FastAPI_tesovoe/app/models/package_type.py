from sqlalchemy import Column, Integer, String
from app.database import Base

class PackageType(Base):
    __tablename__ = "package_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<PackageType(id={self.id}, name={self.name})>"