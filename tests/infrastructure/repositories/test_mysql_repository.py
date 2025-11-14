from pytest_mock import MockerFixture

from infrastructure import MySQLRepository


class TestMySQLRepository:
    def _settings(self, mocker: MockerFixture):
        self.database = mocker.MagicMock()
        self.log = mocker.Mock()
        self.event_db = ('test event', '2025-01-01', '2025-12-31', 100, 50, 5)
        self.ticket_db = ('0888c354', 'e4d1', '2025-11-13', 1, '2025-11-13', '505cd7bc')

    def test_get_event_by_id(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.fetchone.return_value = self.event_db

        repository = MySQLRepository(self.database, self.log)
        data = repository.get_event_by_id('mock_id')

        assert isinstance(data, tuple)
        assert data[0] == 'test event'

    def test_get_event_by_name(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.fetchone.return_value = self.event_db

        repository = MySQLRepository(self.database, self.log)
        data = repository.get_event_by_name('mock_id')

        assert isinstance(data, tuple)
        assert data[0] == 'test event'

    def test_get_ticket_by_code(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.fetchone.return_value = self.ticket_db

        repository = MySQLRepository(self.database, self.log)
        data = repository.get_ticket_by_code('mock_id')

        assert isinstance(data, tuple)
        assert data[0] == '0888c354'

    def test_create_event(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        event = mocker.Mock()
        event.name = ''
        event.start_date = ''
        event.end_date = ''
        event.total_tickets = ''

        repository = MySQLRepository(self.database, self.log)
        data = repository.create_event('mock_id', event)

        assert isinstance(data, bool)
        assert data

    def test_update_event(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        event = mocker.Mock()
        event.name = ''
        event.start_date = ''
        event.end_date = ''
        event.total_tickets = ''

        repository = MySQLRepository(self.database, self.log)
        data = repository.update_event('mock_id', event)

        assert isinstance(data, bool)
        assert data

    def test_delete_event_by_id(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        repository = MySQLRepository(self.database, self.log)
        data = repository.delete_event_by_id('mock_id')

        assert isinstance(data, bool)
        assert data

    def test_create_ticket(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        ticket = {'id': '', 'code': '', 'sale_date': '', 'event_id': ''}

        repository = MySQLRepository(self.database, self.log)
        data = repository.create_ticket(ticket)

        assert isinstance(data, bool)
        assert data

    def test_update_ticket(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        ticket = {'exchange': '', 'exchange_date': ''}

        repository = MySQLRepository(self.database, self.log)
        data = repository.update_ticket('mock_id', ticket)

        assert isinstance(data, bool)
        assert data

    def test_update_event_tickets_sold(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        repository = MySQLRepository(self.database, self.log)
        data = repository.update_event_tickets_sold('mock_id', 10)

        assert isinstance(data, bool)
        assert data

    def test_update_event_tickets_exchanged(self, mocker: MockerFixture):
        self._settings(mocker)

        self.database.return_value.__enter__.\
            return_value.get_session.\
                return_value.cursor.\
                    return_value.rowcount = True

        repository = MySQLRepository(self.database, self.log)
        data = repository.update_event_tickets_exchanged('mock_id', 10)

        assert isinstance(data, bool)
        assert data
