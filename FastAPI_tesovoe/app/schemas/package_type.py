from pydantic import BaseModel

class PackageTypeBase(BaseModel):
    name: str

class PackageTypeCreate(PackageTypeBase):
    pass

class PackageType(PackageTypeBase):
    id: int

    class Config:
        orm_mode = True 