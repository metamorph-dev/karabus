from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.orders.enums import OrderStatus
from app.apps.orders.exceptions import NotEnoughSeats
from app.apps.orders.schemas import CreateOrderRequest
from app.apps.trips.services.read_trip import read_trip
from app.models import Order
from app.models import Passenger
from app.models import Trip
from app.models import User


async def create_order(session: AsyncSession, data: CreateOrderRequest, user: User | None = None) -> Order:
    trip = await read_trip(session, data.trip_id)

    passengers_count = len(data.passengers)
    query = update(Trip).where(Trip.id == trip.id).values(seats_left=Trip.seats_left - passengers_count)

    try:
        await session.execute(query)
    except IntegrityError as exc:
        raise NotEnoughSeats from exc

    order = Order(
        trip=trip,
        user=user,
        price=data.price,
        status=OrderStatus.PENDING,
        passengers=[
            Passenger(
                first_name=passenger.first_name,
                last_name=passenger.last_name,
                ticket_price=passenger.ticket_price,
                age=passenger.age,
            )
            for passenger in data.passengers
        ],
    )

    session.add(order)
    await session.flush()
    return order
