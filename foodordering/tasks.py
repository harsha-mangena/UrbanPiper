from .models import Store, User
from celery import shared_task
from .serializers import *
from time import sleep
import logging
import structlog

from .serializers import *


log = structlog.get_logger(__name__)


@shared_task()
def create_store(pk, store_data):
    try:
        # import pdb ; pdb.set_trace()
        user = User.objects.get(pk=pk)
        store_data['merchant'] = user
        Store.objects.create(**store_data)
    
    except Exception as e:
        log.info("Celery_Store_Creation", error = str(e))
    


@shared_task()
def create_order(pk, order_data):
    try:
        user = User.objects.get(pk=pk)
        order_data['user'] = user
        Order.objects.create(**order_data)

    except Exception as e:
        log.info("Celery_Order_Creation", error = str(e))
