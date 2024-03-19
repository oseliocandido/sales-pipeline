from faker import Faker
from typing import List

fake_generator = Faker()


def generate_fake_data(records: int) -> List[dict]:
    for _ in range(records):
        pass
    return None


print(fake_generator.name())

if __name__ == "__main__":
    data = generate_fake_data()


# - nan string instead None
# - Additional double quote

# Bronze
# # - Only Accepted Values
# Silver
# # - Unecessary Columns\
#  Upper-LowerCase
# # - string in numeric types and vice versa
# # - Expected this format as string  in timestamp fields
# #   -- Tue Dec 30 2014 12:00:00 GMT-0800 (PST)

# Bronze to silver
# # - Duplicate Primary keys
