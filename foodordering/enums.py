from enum import Enum

class OrderStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class userType(Enum):
    CUSTOMER = "CUSTOMER"
    MERCHANT = "MERCHANT"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]