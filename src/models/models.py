from pydantic import BaseModel, Field, field_validator, PositiveInt
from enum import Enum
from datetime import datetime
from typing import Optional


class CategoryEnum(Enum):
    Accessories = "Accessory"
    Bikes = "Bikes"
    Clothing = "Clothing"
    Components = "Components"


class Products(BaseModel):
    ProductKey: PositiveInt
    Product: str
    Standard_Cost: str = Field(alias="Standard Cost")
    Color: Optional[str]
    Subcategory: str
    Category: CategoryEnum = Field(
        description="Category of the product", choices=CategoryEnum
    )
    Background_Color: str = Field(default=None, alias="Background Color", max_length=7)
    Format_Font_Color_Format: Optional[str] = None


class Sales(BaseModel):
    SalesOrderNumber: str
    ProductKey: int
    Quantity: PositiveInt
    Unit_Price: str = Field(alias="Unit Price")

    @field_validator("Unit_Price")
    @classmethod
    def parse_currency_string(cls, value):
        if value[0] == "$":
            try:
                value = float(value.replace(",", "").replace("$", ""))
                if value < 0:
                    raise ValueError("Not Allowed Negative Currency")
            except ValueError:
                raise ValueError("Invalid currency format")
            return value
        else:
            raise ValueError("No $ as first char")


class Target(BaseModel):
    EmployeeID: int
    Target: str
    TargetMonth: str

    @field_validator("TargetMonth")
    @classmethod
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%A, %B %d, %Y")
        except:
            raise ValueError("Invalid date format")
        return value

    @field_validator("Target")
    @classmethod
    def parse_currency_string(cls, value):
        if value[0] == "$":
            try:
                value = float(value.replace(",", "").replace("$", ""))
                if value < 0:
                    raise ValueError("Not Allowed Negative Currency")
            except ValueError:
                raise ValueError("Invalid currency format")
            return value
        else:
            raise ValueError("No $ as first char")


class SalesOrder(BaseModel):
    SalesOrderNumber: str
    OrderDate: str
    ResellerKey: int
    EmployeeKey: int
    SalesTerritoryKey: int

    @field_validator("OrderDate")
    @classmethod
    def parse_order_date(cls, value):
        try:
            datetime.strptime(value, "%A, %B %d, %Y")
        except:
            raise ValueError("Invalid date format")
        return value


class SalesPerson(BaseModel):
    EmployeeKey: int
    EmployeeID: int
    Salesperson: str
    Title: str
    UPN: str
