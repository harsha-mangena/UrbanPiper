import structlog
from rest_framework import serializers

logger = structlog.get_logger()

def validate_order(data):
    
    logger.msg('Validating the order items', data=data)

    store_id = data['items'].store.pk

    remaining_store_id = [item.store.pk for item in data['items'][1:]]

    for pk in remaining_store_id:
        if pk != store_id:
            raise serializers.ValidationError(
                {"items": "Item(s) do not belong to the selected Merchant."})





