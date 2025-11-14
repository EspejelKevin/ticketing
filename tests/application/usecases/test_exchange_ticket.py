from pytest_mock import MockerFixture
import pytest

from datetime import datetime
import datetime as dt

from application import ExchangeTicket
from domain import Response, ResourceNotFoundError, ResourceConflictError, InternalServerError


class TestExchangeTicket:
    def _settings(self, mocker: MockerFixture):
        self.log = mocker.Mock()
        self.db_service = mocker.Mock()
        self.ticket_db = ['ticket_id_mock', 'ticket_code_mock', datetime.now(), False, datetime.now(), 'event_id_mock']
        self.event_db = ['event_name_mock', datetime.now(), datetime.now(), 300, 100, 50]
    
    def test_ticket_not_found(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_ticket_by_code.return_value = None

        self.use_case = ExchangeTicket(self.db_service, self.log)

        with pytest.raises(ResourceNotFoundError) as ex:
            self.use_case.execute('code_ticket_mock')

        assert ex.value.status_code == 404
        assert ex.value.data['message'] == 'the resource code_ticket_mock was not found, try again.'

    def test_find_event_by_ticket_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_ticket_by_code.return_value = self.ticket_db
        self.db_service.get_event_by_id.return_value = None

        self.use_case = ExchangeTicket(self.db_service, self.log)

        with pytest.raises(ResourceNotFoundError) as ex:
            self.use_case.execute('code_ticket_mock')

        assert ex.value.status_code == 404
        assert ex.value.data['message'] == 'the resource event_id_mock was not found, try again.'

    def test_ticket_exchanged_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.ticket_db[3] = True
        self.db_service.get_ticket_by_code.return_value = self.ticket_db
        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = ExchangeTicket(self.db_service, self.log)

        with pytest.raises(ResourceConflictError) as ex:
            self.use_case.execute('code_ticket_mock')

        assert ex.value.status_code == 409
        assert ex.value.data['message'] == 'ticket code_ticket_mock status: it already was exchanged'

    def test_current_date_out_of_range(self, mocker: MockerFixture):
        self._settings(mocker)

        self.event_db[1] = datetime.now() + dt.timedelta(days=1)
        self.db_service.get_ticket_by_code.return_value = self.ticket_db
        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = ExchangeTicket(self.db_service, self.log)

        with pytest.raises(ResourceConflictError) as ex:
            self.use_case.execute('code_ticket_mock')

        assert ex.value.status_code == 409
        assert ex.value.data['message'] == 'an error ocurred while changing the ticket status, because the current_date out of range'

    def test_update_ticket_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_ticket_by_code.return_value = self.ticket_db
        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.update_ticket.return_value = None

        self.use_case = ExchangeTicket(self.db_service, self.log)

        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute('code_ticket_mock')

        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while updating ticket: code_ticket_mock'

    def test_update_event_tickets_exchanged_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_ticket_by_code.return_value = self.ticket_db
        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.update_ticket.return_value = True
        self.db_service.update_event_tickets_exchanged.return_value = None

        self.use_case = ExchangeTicket(self.db_service, self.log)

        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute('code_ticket_mock')

        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while updating tickets exchanged of event: event_id_mock'

    def test_execute(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_ticket_by_code.return_value = self.ticket_db
        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.update_ticket.return_value = True
        self.db_service.update_event_tickets_exchanged.return_value = True

        self.use_case = ExchangeTicket(self.db_service, self.log)
        response = self.use_case.execute('code_ticket_mock')

        assert isinstance(response, Response)
        assert response.data['exchange']
        assert isinstance(response.data['exchange_date'], datetime)
        assert response.status_code == 200
    