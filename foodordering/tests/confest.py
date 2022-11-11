import pytest 
from foodordering.models import User

@pytest.fixture
def data():
    customer = User.objects.create_user(username="consumer", email="consumer@gmail.com", password="password@123", user_type="Customer", is_active=True)
    
    return customer 

