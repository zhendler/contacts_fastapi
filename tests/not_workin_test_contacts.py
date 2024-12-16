from unittest.mock import AsyncMock

import aioredis
import pytest
from fastapi_limiter import FastAPILimiter
from httpx import AsyncClient, ASGITransport

from config.general import settings
from main import app
from src.contacts.models import Contact
#------------------------------------------------------------------
# не можу зрозуміти проблему , так як немає часу топоки залишаю так(
# --------------------------------------------------------------------
# @pytest.fixture(scope="module")
# async def setup_redis():
#     redis = aioredis.from_url(settings.redis_url, encoding="utf-8")
#     await FastAPILimiter.init(redis)
#     yield redis
#     await redis.close()

# @pytest.mark.asyncio
# async def test_create_contact(test_user, auth_header, override_get_db, monkeypatch):
#     user_id = test_user.id
#     mock_cache = AsyncMock()
#     monkeypatch.setattr("src.contacts.routers.invalidate_get_contacts_repo_cache", mock_cache)
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
#         response = await ac.post("/contacts/", json={
#             "first_name": "John",
#             "last_name": "Doe",
#             "email": "john.doe@example.com",
#             "phone_number": "1234567890",
#             "birthday": "1990-01-01",
#             "additional_info": "This is a sample contact."
#         }, headers=auth_header)
#         assert response.status_code == 200
#         data = response.json()
#         assert data['first_name'] == "John"
#         assert data['last_name'] == "Doe"
#         mock_cache.assert_called_once_with(user_id)




# @pytest.mark.asyncio
# async def test_get_contact(
#     override_get_db, test_user_contact: Contact, auth_header, monkeypatch
# ):
#     mock_cache = AsyncMock()
#     monkeypatch.setattr("src.contacts.routers.cache", mock_cache)
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#
#         # Then, retrieve the contact by ID
#         response = await ac.get(
#             f"/contacts/{test_user_contact.id}", headers=auth_header
#         )
#
#     assert response.status_code == 200
#     data = response.json()
#     assert data["first_name"] == test_user_contact.first_name
#     assert data["last_name"] == test_user_contact.last_name