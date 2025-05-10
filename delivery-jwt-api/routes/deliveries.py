from fastapi import status
from fastapi.responses import JSONResponse
from validators import DeliveryUpdate, DeliveryBase

from misc import problemResponse, successResponse
from loader import AdapterDB, app
from config import PROHIBITED_DATA_UPDATE_DELIVERY


@app.patch("/deliveries/{order_id}")
async def updateDelivery(order_id: int, delivery_data: DeliveryUpdate) -> JSONResponse:
    """Обновление данных о доставке

    :param order_id: ID доставки
    :type order_id: int
    :param delivery_data: Словарь с data для обновления
    :type delivery_data: DeliveryUpdate
    :return: Ответ в формате JSON
    :rtype: JSONResponse
    """
    update_data = delivery_data.model_dump(exclude_unset=True)
    prohibited_fields = [field for field in update_data if field in PROHIBITED_DATA_UPDATE_DELIVERY]
    if prohibited_fields:
        return problemResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                title="Prohibited field modification",
                detail=f"Cannot update restricted fields: {', '.join(prohibited_fields)}",
                invalid_params=[{"field": field, "reason": "read-only"} for field in prohibited_fields]
            )
    try:
        success = await AdapterDB.updateDelivery(order_id, **update_data)
        if not success:
            return problemResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    title="Delivery not found",
                    detail=f"Delivery with id {order_id} does not exist"
                )
    except Exception as e:
        return problemResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            title="Invalid input data",
            detail=str(e)
        )

    return successResponse(status_code=status.HTTP_200_OK, id=order_id)