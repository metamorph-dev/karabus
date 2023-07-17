from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apps.trips.schemas import CreateTripRequest
from app.models import Bus
from app.models import Trip
from app.models import TripStop


async def create_trip(session: AsyncSession, bus: Bus, data: CreateTripRequest) -> Trip:
    trip = Trip(
        name=data.name,
        price=data.price,
        bus=bus,
        seats_left=bus.seats_quantity,
        stops=[TripStop(city_id=stop.city_id, datetime=stop.datetime) for stop in data.stops],
    )
    session.add(trip)

    try:
        await session.flush()
    except IntegrityError:
        pass

    return trip
