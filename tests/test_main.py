from typing import NoReturn

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_say_hello(client: AsyncClient) -> NoReturn:
    response = await client.get("/hello-world/")
    assert response.status_code == 200
    assert response.json().get("message") == "Hello, world!"
