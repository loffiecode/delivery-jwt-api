from fastapi import status
from fastapi.responses import JSONResponse

from misc import problemResponse, successResponse
from validators import OrderCreate
from loader import AdapterDB, app


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteOrder(order_id: int) -> JSONResponse:
    """Удаляет Order

    :param order_id: ID ордера
    :type order_id: int
    :return: Ответ в формате JSON
    :rtype: JSONResponse
    """
    success = await AdapterDB.deleteOrder(order_id)
    if not success:
        return problemResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Order not found",
            detail=f"Order with id {order_id} does not exist",
        )
    return successResponse(status_code=status.HTTP_200_OK, id=order_id)

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def createOrder(order_data: OrderCreate) -> JSONResponse:
    """Создание нового Order

    :param order_data: Информация для создания заказа
    :type order_data: OrderCreate
    :return: Ответ в формате JSON
    :rtype: JSONResponse
    """
    try:
        result = await AdapterDB.createOrder(
            name=order_data.name,
            pickup=order_data.pickUpAddress,
            delivery=order_data.deliveryAddress,
            weight=order_data.weight,
            dimensions=order_data.dimensions,
            description=order_data.description
        )
                
        return successResponse(
            id=result.ID,
            status_code=status.HTTP_201_CREATED
        )
        
    except ValueError as e:
        return problemResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            title="Invalid input data",
            detail=str(e),
        )
    except Exception as e:
        return problemResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            title="Internal server error",
            detail=f"An unexpected error occurred: {e}",
        )

@app.get("/orders/{order_id}")
async def getOrder(order_id: int) -> JSONResponse:
    """Получение информации о заказе и его доставке

    :param order_id: ID заказа
    :type order_id: int
    :return: Ответ в формате JSON
    :rtype: JSONResponse
    """
    order = await AdapterDB.getOrder(order_id)
    if not order:
        return problemResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Order not found",
            detail=f"Order with id {order_id} not found",
        )
    return successResponse(
        status_code=status.HTTP_200_OK,
        id=order.ID,
        description=order.Description,
        status=order.delivery.Status,
        target_time_delivery=order.delivery.TargetTimeDelivery.isoformat() \
                 if order.delivery.TargetTimeDelivery else None,
        dimensions=order.Dimensions,
        weight=order.Weight,
        deliveryAddress=order.DeliveryAddress,
        pickUpAddress=order.PickUpAddress,
        name=order.Name,
        creation_date=order.CreationDate.isoformat()   
    )