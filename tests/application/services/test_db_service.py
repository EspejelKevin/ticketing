from pytest_mock import MockerFixture

from application import DBService


class TestDBService:
    def _settings(self, mocker: MockerFixture):
        event = {
            'id': '22f93764-8551-4e96-af6d-66a6254924bc',
            'name': 'Pytest Event Mock',
            'start_date': '2025-11-14 00:00:00',
            'end_date': '2025-11-15 00:00:00',
            'total_tickets': 300,
            'total_tickets_sold': 0,
            'total_tickets_exchange': 0
        }

        ticket = {
            'id': '088bc354-e6d1-439c-a075-c21932e2d0d5',
            'code': '203588607d20416997792254969300575088742',
            'sale_date': '2025-11-13 09:32:03',
            'exchange': 1,
            'exchange_date': '2025-11-13 09:39:41',
            'event_id': '505cd7bc-493d-4c62-a0e0-d09f232b2f02'
        }

        self.db_repository = mocker.Mock()
        self.db_repository.get_event_by_id = mocker.Mock(return_value=event)
        self.db_repository.get_event_by_name = mocker.Mock(return_value=event)
        self.db_repository.get_ticket_by_code = mocker.Mock(return_value=ticket)
        self.db_repository.create_event = mocker.Mock(return_value=True)
        self.db_repository.update_event = mocker.Mock(return_value=True)
        self.db_repository.delete_event_by_id = mocker.Mock(return_value=True)
        self.db_repository.create_ticket = mocker.Mock(return_value=True)
        self.db_repository.update_ticket = mocker.Mock(return_value=True)
        self.db_repository.update_event_tickets_sold = mocker.Mock(return_value=True)
        self.db_repository.update_event_tickets_exchanged = mocker.Mock(return_value=True)

        self.db_service = DBService(self.db_repository)

    def test_get_event_by_id(self, mocker: MockerFixture):
        self._settings(mocker)

        event = self.db_service.get_event_by_id('22f93764-8551-4e96-af6d-66a6254924bc')
        
        assert isinstance(event, dict)
        assert event['id'] == '22f93764-8551-4e96-af6d-66a6254924bc'
        assert event['name'] == 'Pytest Event Mock'
        assert event['total_tickets'] == 300

    def test_get_event_by_name(self, mocker: MockerFixture):
        self._settings(mocker)

        event = self.db_service.get_event_by_name('22f93764-8551-4e96-af6d-66a6254924bc')
        
        assert isinstance(event, dict)
        assert event['id'] == '22f93764-8551-4e96-af6d-66a6254924bc'
        assert event['name'] == 'Pytest Event Mock'
        assert event['total_tickets_sold'] == 0

    def test_get_ticket_by_code(self, mocker: MockerFixture):
        self._settings(mocker)

        ticket = self.db_service.get_ticket_by_code('203588607d20416997792254969300575088742')
        
        assert isinstance(ticket, dict)
        assert ticket['code'] == '203588607d20416997792254969300575088742'
        assert ticket['exchange'] == 1

    def test_create_event(self, mocker):
        self._settings(mocker)
        result = self.db_service.create_event('event_id', {})
        assert result

    def test_update_event(self, mocker):
        self._settings(mocker)
        result = self.db_service.update_event('event_id', {})
        assert result

    def test_delete_event_by_id(self, mocker):
        self._settings(mocker)
        result = self.db_service.delete_event_by_id('event_id')
        assert result

    def test_create_ticket(self, mocker):
        self._settings(mocker)
        result = self.db_service.create_ticket({})
        assert result

    def test_update_ticket(self, mocker):
        self._settings(mocker)
        result = self.db_service.update_ticket('code', {})
        assert result

    def test_update_event_tickets_sold(self, mocker):
        self._settings(mocker)
        result = self.db_service.update_event_tickets_sold('event_id', 10)
        assert result

    def test_update_event_tickets_exchanged(self, mocker):
        self._settings(mocker)
        result = self.db_service.update_event_tickets_exchanged('event_id', 10)
        assert result
