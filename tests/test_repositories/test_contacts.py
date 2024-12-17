import unittest
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
from pydantic import ValidationError

from src.contacts.schema import ContactCreate
from src.contacts.models import Contact
from src.contacts.repos import ContactRepository


class TestContactRepository(unittest.IsolatedAsyncioTestCase):
    async def test_create_contact(self):
        # Arrange
        mock_session = MagicMock()
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        # Вхідні дані
        contact_data = ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            b_date="1990-01-01"
        )

        owner_id = 1

        # Очікуваний результат
        expected_contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", owner_id=owner_id)

        # Mock повернення new_contact під час refresh
        mock_session.refresh.side_effect = lambda obj: setattr(obj, "id", 1)

        # Репозиторій
        repo = ContactRepository(mock_session)

        # Act
        result = await repo.create_contact(contact_data, owner_id)

        # Assert
        mock_session.add.assert_called_once()  # Перевірка виклику add()
        mock_session.commit.assert_awaited_once()  # Перевірка виклику commit()
        mock_session.refresh.assert_awaited_once()  # Перевірка виклику refresh()
        self.assertEqual(result.first_name, expected_contact.first_name)
        self.assertEqual(result.last_name, expected_contact.last_name)
        self.assertEqual(result.email, expected_contact.email)
        self.assertEqual(result.owner_id, expected_contact.owner_id)
        self.assertEqual(result.id, 1)

    async def test_delete_contact_not_found(self):
        # Arrange
        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=None)  # Повертатимемо None, щоб імітувати відсутність контакту

        repo = ContactRepository(mock_session)

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await repo.delete_contact(1)

        # Перевірка, що статус код 404
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Contact not found")

        mock_session.get.assert_awaited_once_with(Contact, 1)  # Перевірка виклику get()
        mock_session.delete.assert_not_called()  # Перевірка, що delete не було викликано
        mock_session.commit.assert_not_called()  # Перевірка, що commit не було викликано









if __name__ == "__main__":
    unittest.main()
