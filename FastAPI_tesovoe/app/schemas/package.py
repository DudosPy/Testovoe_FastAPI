from pydantic import BaseModel
from typing import Optional, List

class PackageBase(BaseModel):
    name: str
    weight: float
    content_cost: float
    package_type_id: int

class PackageCreate(PackageBase):
    pass  

class Package(PackageBase):
    id: int
    delivery_cost: Optional[float] = None
    session_id: str

    class Config:
        orm_mode = True
