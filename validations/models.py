from pydantic import BaseModel, Field, field_validator, PositiveFloat
from enum import Enum
from datetime import datetime, date
from typing import Optional

# Money validation
# Sure, here are some validation rules for monetary values:
# The monetary value should start with a currency symbol (e.g., '$' for US dollars).
# The monetary value should have a decimal point followed by exactly two digits for cents (e.g., '.00' in '$10.00').
# The monetary value may have a negative sign at the beginning (e.g., '-$10.00').


class CategoryEnum(Enum):
    Accessories = "Accessories"
    Bikes = "Bikes"
    Clothing = "Clothing"
    Components = "Components"


class Products(BaseModel):
    ProductKey: int
    Product: str
    Category: CategoryEnum = Field(
        description="Category of the product", choices=CategoryEnum
    )
    Standard_Cost: str = Field(alias="Standard Cost")
    Color: Optional[str]


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


class SalesOrder(BaseModel):
    SalesOrderNumber: str
    OrderDate: str
    ProductKey: int
    ResellerKey: int
    EmployeeKey: int
    SalesTerritoryKey: int
    Quantity: int
    UnitPrice: str = Field(alias="Unit Price")
    Sales: str
    Cost: str

    @field_validator("OrderDate")
    @classmethod
    def parse_order_date(cls, value):
        try:
            datetime.strptime(value, "%A, %B %d, %Y")
        except:
            raise ValueError("Invalid date format")
        return value

    @field_validator("UnitPrice", "Sales", "Cost")
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
            raise ValueError("No $ in first char")


# Ideias
# -- Replace wrong string by correct ones
# --


# # Some signatures have quotes around them, unneeded
# df["signature"] = df["signature"].str.replace('"', "")
# if re.search("Discont", str(row["price"])):


#     # Replacing ? device prices with -1
#     if re.search("\\?", str(row["price"])):
#         row["price"] = -1

#     # Some prices have models embedded to them, this replaces with only price
#     # Ex: 3000(HE1000) gives 3000
#     if re.search("[a-zA-Z]", str(row["price"])):
#         row["price"] = list(filter(None, re.split(r"(\d+)", str(row["price"]))))[0]

#         # Some are still text even after splits and earlier cleanses
#         if re.search("[a-zA-Z]", str(row["price"])):
#             row["price"] = -1

#     # Replace star text rating with number. If no stars, replace with -1
#     row["value_rating"] = len(row["value_rating"]) if row["value_rating"] else -1

# return df.to_dict("records")


# if __name__ == "__main__":
# headphones_file = "/tmp/headphones-bronze.csv"
# iems_file = "/tmp/iems-bronze.csv"

# iems_list = read_csv_as_dicts(iems_file)
# headphones_list = read_csv_as_dicts(headphones_file)

# # Sanitize both CSV files with similar parameters
# iems_list_sanitized = sanitize_data(iems_list)
# headphones_list_sanitized = sanitize_data(headphones_list)

# # Validates all headphones/iems in a list based on the validators
# # defined in the respective PyDantic models
# try:
#     iems_list = [InEarMonitor.parse_obj(iem) for iem in iems_list_sanitized]
# except ValidationError as exception:
#     print(f"IEM - {exception}")

# try:
#     headphones_list = [
#         Headphone.parse_obj(headphone) for headphone in headphones_list_sanitized
#     ]
# except ValidationError as exception:
#     print(f"Headphone - {exception}")

# convert_to_csv(device_data=iems_list_sanitized, device_type="iems", data_level="silver")
# convert_to_csv(
#     device_data=headphones_list_sanitized, device_type="headphones", data_level="silver"
# )
