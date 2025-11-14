from pytest_mock import MockerFixture
import pytest

from application import CreateEvent
from domain import Response, ResourceAlreadyExistsError, InternalServerError


class TestCreateEvent:
    def _settings(self, mocker: MockerFixture):
        self.log = mocker.Mock()
        self.db_service = mocker.Mock()
        self.event_input = mocker.Mock()
        self.event_input.name = 'event_name_mock'
        self.event_input.start_date = 'event_date_mock'
        self.event_input.end_date = 'event_date_mock'

    def test_execute(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_name.return_value = None
        self.db_service.create_event.return_value = True

        self.use_case = CreateEvent(self.db_service, self.log)
        response = self.use_case.execute(self.event_input)
        
        assert isinstance(response, Response)
        assert response.data['name'] == 'event_name_mock'
        assert response.data['start_date'] == 'event_date_mock'
        assert response.data['end_date'] == 'event_date_mock'
        assert response.status_code == 201
    
    def test_event_already_exists(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_name.return_value = True

        self.use_case = CreateEvent(self.db_service, self.log)
        
        with pytest.raises(ResourceAlreadyExistsError) as ex:
            self.use_case.execute(self.event_input)
        
        assert ex.value.status_code == 409
        assert ex.value.data['message'] == 'this resource event_name_mock already exists, try again.'

    def test_error_while_creating_event(self, mocker: MockerFixture):
        self._settings(mocker)

        self.db_service.get_event_by_name.return_value = None
        self.db_service.create_event.return_value = False

        self.use_case = CreateEvent(self.db_service, self.log)
        
        with pytest.raises(InternalServerError) as ex:
            self.use_case.execute(self.event_input)
        
        assert ex.value.status_code == 500
        assert ex.value.data['message'] == 'error while creating event event_name_mock'
