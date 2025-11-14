from pytest_mock import MockerFixture
import pytest

from datetime import datetime
import datetime as dt

from application import EventDetails
from domain import Response, ResourceNotFoundError, InternalServerError


class TestEventDetails:
    def _settings(self, mocker: MockerFixture):
        self.log = mocker.Mock()
        self.db_service = mocker.Mock()
        self.event_db = ['event_name_mock', datetime.now(), datetime.now(), 100, 100, 50]

    def test_execute(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = EventDetails(self.db_service, self.log)
        response = self.use_case.execute('event_id_mock')
        
        assert isinstance(response, Response)
        assert response.data['name'] == 'event_name_mock'
        assert response.data['total_tickets_available'] == 0
        assert response.data['total_tickets_sold'] == 100
        assert response.status_code == 200

    def test_event_not_found(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = None

        self.use_case = EventDetails(self.db_service, self.log)

        with pytest.raises(ResourceNotFoundError) as ex:
            self.use_case.execute('event_id_mock')
        
        assert ex.value.status_code == 404
        assert ex.value.data['message'] == 'the resource event_id_mock was not found, try again.'
