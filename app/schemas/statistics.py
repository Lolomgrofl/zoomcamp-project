from pydantic import BaseModel, ConfigDict


class BaseStatistics(BaseModel):
    average_price: float
    median_price: float
    total_properties: int
    average_price_per_sqft: float


class PropertyModel(BaseModel):
    state: str
    address: str
    price: float | int
    bathrooms: float | int
    geometry: str
    city: str
    propertyid: int
    zipcode: str
    bedrooms: float | int
    squarefeet: float | int

    model_config = ConfigDict(from_attributes=True)
