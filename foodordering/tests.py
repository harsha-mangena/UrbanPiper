import pytest
from pdb import Pdb
from rest_framework.test import APIClient

from .models import Item, Store, User


'''
Test for User Registration
'''
@pytest.mark.django_db
def test_for_user_registratin():
    user = User.objects.create_user('test', 'test@test.com', 'test')
    assert user.username == 'test' 

@pytest.mark.django_db

