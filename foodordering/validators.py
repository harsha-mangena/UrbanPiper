import structlog

logger = structlog.get_logger()

def validate_order(data):
    
    logger.msg('Validating the order items', data=data)

    store_id = data['store'].id

    items_store_id = [item.store.id for item in data['items']]

    for item_store_id in items_store_id:
        if item_store_id != store_id:
            raise structlog.exceptions.InvalidStructureError(
                message='Invalid item in the store',
                data=data,
                store_id=store_id,
                item_store_id=item_store_id,
            )


