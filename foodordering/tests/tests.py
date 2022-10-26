import pytest
from pdb import Pdb
from rest_framework.test import APIClient

from foodordering.models import Item, Store, User


client = APIClient()
'''
Test for User Registration
'''
@pytest.mark.django_db
def test_for_customer_registration():
    payload = {"name" : "Customer", 
               "email": "consumer@gmail.com",
               "username": "consumer", 
               "password": "password@123",
               "retype_password": "password@123",
               "user_type": "Customer",
               "is_active": True,
               }
    response = client.post("/register/", payload)
    assert response.status_code == 201

'''
Test for Merchant Registration
'''
@pytest.mark.django_db
def test_for_customer_registration():
    payload = {"name" : "Merchant", 
               "email": "merchant@gmail.com",
               "username": "merchant", 
               "password": "password@123",
               "retype_password": "password@123",
               "user_type": "Merchant",
               "is_active": True,
               }
    response = client.post("/register/", payload)
    assert response.status_code == 201

