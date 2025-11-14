from pytest_mock import MockerFixture
import pytest

from datetime import datetime
import datetime as dt

from application import UpdateEvent
from domain import (Response, ResourceNotFoundError,
                    ResourceConflictError, InternalServerError, BadRequestError)


class TestUpdateEvent:
    def _settings(self, mocker: MockerFixture):
        self.log = mocker.Mock()
        self.db_service = mocker.Mock()
        self.event_input = mocker.Mock()
        self.event_input.name = 'event_name_mock'
        self.event_input.start_date = datetime.now()
        self.event_input.end_date = datetime.now()
        self.event_input.total_tickets = 200
        self.event_db = ['event_name_mock', datetime.now(), datetime.now(), 300, 100, 50]

    def test_find_event_by_id_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = None

        self.use_case = UpdateEvent(self.db_service, self.log)

        with pytest.raises(ResourceNotFoundError) as ex:
            self.use_case.execute('mock_id_event', self.event_input)

        assert ex.value.status_code == 404
        assert ex.value.data['message'] == 'the resource mock_id_event was not found, try again.'

    def test_end_date_validation_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = UpdateEvent(self.db_service, self.log)

        with pytest.raises(BadRequestError) as ex:
            self.event_input.end_date = datetime.now() - dt.timedelta(days=2)
            self.use_case.execute('mock_id_event', self.event_input)

        assert ex.value.status_code == 400
        assert ex.value.data['message'] == 'new end_date can not be less than start_date initial'

    def test_total_tickets_validation_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = UpdateEvent(self.db_service, self.log)

        with pytest.raises(BadRequestError) as ex:
            self.event_input.total_tickets = 50
            self.use_case.execute('mock_id_event', self.event_input)

        assert ex.value.status_code == 400
        assert ex.value.data['message'] == 'total_tickets can not be less than total_tickets_sold'

    def test_event_finished_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.event_db[2] = datetime.now() - dt.timedelta(days=2)
        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = UpdateEvent(self.db_service, self.log)

        with pytest.raises(ResourceConflictError) as ex:
            self.use_case.execute('mock_id_event', self.event_input)

        assert ex.value.status_code == 409
        assert ex.value.data['message'] == 'the event event_name_mock can not be updated becasue has finished'

    def test_update_event_error(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.update_event.return_value = None

        self.use_case = UpdateEvent(self.db_service, self.log)

        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute('mock_id_event', self.event_input)

        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while updating event mock_id_event'

    def test_execute(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db
        self.db_service.update_event.return_value = True

        self.use_case = UpdateEvent(self.db_service, self.log)
        response = self.use_case.execute('mock_id_event', self.event_input)

        assert isinstance(response, Response)
        assert response.status_code == 200
