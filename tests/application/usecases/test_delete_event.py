from pytest_mock import MockerFixture
import pytest

from datetime import datetime
import datetime as dt

from application import DeleteEvent
from domain import Response, ResourceNotFoundError, InternalServerError


class TestDeleteEvent:
    def _settings(self, mocker: MockerFixture):
        self.log = mocker.Mock()
        self.db_service = mocker.Mock()
        self.event_db = ['event_name_mock', datetime.now(), datetime.now(), 300, 100, 50]
        self.event_db_to_delete = ['event_name_mock_delete', datetime.now(), datetime.now()-dt.timedelta(days=2), 300, 100, 50]

    def test_execute(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db

        self.use_case = DeleteEvent(self.db_service, self.log)
        response = self.use_case.execute('event_id_mock')
        
        assert isinstance(response, Response)
        assert response.data['message'] == 'the event can not be delete because is active or has tickets sold'
        assert response.status_code == 200

    def test_event_not_found(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = None

        self.use_case = DeleteEvent(self.db_service, self.log)

        with pytest.raises(ResourceNotFoundError) as ex:
            self.use_case.execute('event_id_mock')
        
        assert ex.value.status_code == 404
        assert ex.value.data['message'] == 'the resource event_id_mock was not found, try again.'

    def test_event_deleted(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db_to_delete
        self.db_service.delete_event_by_id.return_value = True

        self.use_case = DeleteEvent(self.db_service, self.log)
        response = self.use_case.execute('event_id_mock')
        
        assert isinstance(response, Response)
        assert response.data['name'] == 'event_name_mock_delete'
        assert response.data['total_tickets_available'] == 200
        assert response.data['total_tickets_sold'] == 100
        assert response.status_code == 200

    def test_error_while_deleting(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_id.return_value = self.event_db_to_delete
        self.db_service.delete_event_by_id.return_value = False

        self.use_case = DeleteEvent(self.db_service, self.log)
        
        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute('event_id_mock')
        
        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while deleting event event_id_mock'
