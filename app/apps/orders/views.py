from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.apps.orders.exceptions import NotEnoughSeats
from app.apps.orders.schemas import ConfirmPaymentRequest
from app.apps.orders.schemas import CreateOrderRequest
from app.apps.orders.schemas import CreateOrderResponse
from app.apps.orders.schemas import ReadAllOrderResponse
from app.apps.orders.schemas import ReadOrderResponse
from app.apps.orders.use_cases import ConfirmPayment
from app.apps.orders.use_cases import CreateOrder
from app.apps.orders.use_cases import ReadAllOrder
from app.apps.orders.use_cases import ReadMyOrders
from app.apps.orders.use_cases import ReadOrder
from app.base.exceptions import NotFoundError


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(data: CreateOrderRequest, use_case: CreateOrder = Depends()) -> CreateOrderResponse:
    try:
        result = await use_case.execute(data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc))
    except NotEnoughSeats as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc))

    return result


@router.get("/")
async def read_all(use_case: ReadAllOrder = Depends(), offset: int = 0, limit: int = 50) -> ReadAllOrderResponse:
    return ReadAllOrderResponse(orders=[order async for order in use_case.execute(offset, limit)])


@router.get("/my")
async def read_my_orders(use_case: ReadMyOrders = Depends(), offset: int = 0, limit: int = 50) -> ReadAllOrderResponse:
    return ReadAllOrderResponse(orders=[order async for order in use_case.execute(offset, limit)])


@router.get("/{order_id}")
async def read(order_id: int, use_case: ReadOrder = Depends()) -> ReadOrderResponse:
    try:
        result = await use_case.execute(order_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc))

    return result


@router.post("/{order_id}/payment", status_code=status.HTTP_204_NO_CONTENT)
async def create_payment(order_id: int, data: ConfirmPaymentRequest, use_case: ConfirmPayment = Depends()):
    try:
        await use_case.execute(order_id, data.status)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc))
