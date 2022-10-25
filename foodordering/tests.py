import pytest
from pdb import Pdb
from rest_framework.test import APIClient

from .models import Item, Store, User

@pytest.mark.django_db
def test_for_user_registratin():
    user = User.objects.create_user('test', 'test@test.com', 'test')
    store = Store.objects.create(user=user)
    item = Item.objects.create(store=store)
    assert item.store == store

