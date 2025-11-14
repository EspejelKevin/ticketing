from pytest_mock import MockerFixture
import pytest

from datetime import datetime

from application import SellerTicket
from domain import Response, ResourceNotFoundError, ResourceConflictError, InternalServerError


class TestSellerTicket:
    def _settings(self, mocker: MockerFixture):
        self.log = mocker.Mock()
        self.db_service = mocker.Mock()
        self.ticket_input = mocker.Mock()
        self.ticket_input.event_id = 'event_id_mock_from_input'
        self.event_db = ['event_name_mock', datetime.now(), datetime.now(), 300, 100, 50]

    def test_find_event_by_id_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = None

        self.use_case = SellerTicket(self.db_service, self.log)

        with pytest.raises(ResourceNotFoundError) as ex:
            self.use_case.execute(self.ticket_input)

        assert ex.value.status_code == 404
        assert ex.value.data['message'] == 'the resource event_id_mock_from_input was not found, try again.'

    def test_quantity_tickets_sold_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.event_db[4] = 300
        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = SellerTicket(self.db_service, self.log)

        with pytest.raises(ResourceConflictError) as ex:
            self.use_case.execute(self.ticket_input)

        assert ex.value.status_code == 409
        assert ex.value.data['message'] == 'event event_name_mock status: there are not available tickets'

    def test_create_ticket_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.create_ticket.return_value = None

        self.use_case = SellerTicket(self.db_service, self.log)

        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute(self.ticket_input)

        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while creating ticket for event: event_name_mock'

    def test_update_event_tickets_sold_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.create_ticket.return_value = True
        self.db_service.update_event_tickets_sold.return_value = None

        self.use_case = SellerTicket(self.db_service, self.log)

        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute(self.ticket_input)

        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while updating tickets sold of event: event_name_mock'

    def test_execute(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.create_ticket.return_value = True
        self.db_service.update_event_tickets_sold.return_value = True

        self.use_case = SellerTicket(self.db_service, self.log)
        response = self.use_case.execute(self.ticket_input)

        assert isinstance(response, Response)
        assert response.data['event_id'] == 'event_id_mock_from_input'
        assert response.status_code == 201
