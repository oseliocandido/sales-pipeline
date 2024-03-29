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
    Category: CategoryEnum = Field(choices=CategoryEnum)
    Background_Color: str = Field(default=None, alias="Background Color", max_length=7)
    Format_Font_Color_Format: Optional[str] = None


class Sales(BaseModel):
    SalesOrderNumber: str
    ProductKey: PositiveInt
    Quantity: PositiveInt
    Unit_Price: str = Field(alias="Unit Price")
    Cost: str

    @field_validator("Unit_Price", "Cost")
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
    EmployeeID: PositiveInt
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
    ResellerKey: PositiveInt
    EmployeeKey: PositiveInt
    SalesTerritoryKey: PositiveInt

    @field_validator("OrderDate")
    @classmethod
    def parse_order_date(cls, value):
        try:
            datetime.strptime(value, "%A, %B %d, %Y")
        except:
            raise ValueError("Invalid date format")
        return value


class SalesPerson(BaseModel):
    EmployeeKey: PositiveInt
    EmployeeID: PositiveInt
    Salesperson: str
    Title: str
    UPN: str = Field(max_length=320)
